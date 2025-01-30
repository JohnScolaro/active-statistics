import dataclasses
import datetime as dt
import json
import math
import os
from typing import Iterable

import polyline as pl
from PIL import Image as img
from PIL import ImageDraw
from PIL.Image import Image
from stravalib.model import DetailedActivity

Polyline = list[tuple[float, float]]


def create_images(activity_iterator: Iterable[DetailedActivity], path: str) -> None:
    captions: dict[str, str] = {}

    compact_activities = [
        CompactActivity(
            type=activity.type,
            summary_polyline=activity.map.summary_polyline,
            start_date_local=activity.start_date_local,
        )
        for activity in activity_iterator
        if activity.start_date_local is not None
        and activity.map.summary_polyline is not None
    ]
    compact_activities.sort(key=lambda x: x.start_date_local)

    activity_types = set(
        compact_activity.type for compact_activity in compact_activities
    )

    PROPOSED_IMAGE_SIZE = 1200
    BORDER_SIZE_PX = 6
    LINE_THICKNESS = 1

    for activity_type in activity_types:
        image = create_image(
            (
                activity.summary_polyline
                for activity in compact_activities
                if activity.type == activity_type
            ),
            1.0,
            PROPOSED_IMAGE_SIZE,
            BORDER_SIZE_PX,
            LINE_THICKNESS,
        )

        if image is None:
            continue

        image_name = f"{activity_type}_grid.png"
        image_path = os.path.join(path, image_name)
        image.save(image_path, "PNG")
        image.close()

        captions[image_name] = f"A grid of all {activity_type} activities."

        gif_duration_ms = 2000
        gif_fps = 40
        images = create_gif_image(
            [
                activity.summary_polyline
                for activity in compact_activities
                if activity.type == activity_type
            ],
            gif_duration_ms,
            gif_fps,
            PROPOSED_IMAGE_SIZE,
            BORDER_SIZE_PX,
            LINE_THICKNESS,
        )
        gif_name = f"{activity_type}_grid_animation.gif"
        gif_path = os.path.join(path, gif_name)
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=gif_duration_ms / gif_fps,
            loop=0,
        )

        captions[gif_name] = f"An animation of all {activity_type} activities."

    # Create captions
    # Dump the dictionary to a JSON file
    with open(os.path.join(path, "captions.json"), "w") as json_file:
        json.dump(captions, json_file)


def create_image(
    encoded_polylines: Iterable[str],
    polyline_fraction: float = 1.0,
    proposed_image_size: int = 2000,
    border_size_px: int = 1,
    line_thickness: int = 2,
) -> Image | None:
    """
    Creates and returns a PIL image object with all polylines displayed in a grid.

    max_segments_fraction: This is a float between 0 and 1.
        * At 0, nothing is plotted.
        * At 0.5, half the polyline is plotted.

    proposed_image_size: The height and width of the created image in pixels.
        The final image size will very slightly from this, but hopefully not
        too much.

    border_size_px: The size of the border between each individual plot square
        in pixels.

    line_thickness: The thickness of the line which draws the routes in px.
    """
    polylines: list[Polyline] = []
    for encoded_polyline in encoded_polylines:
        polyline: Polyline = pl.decode(encoded_polyline)

        if len(polyline) <= 1:
            # I think we have ran into instances where people have ONLY activities with a single
            # lat-long pair here, which means that the max cheby distance is 0, and then we do a
            # divide by zero. So lets just continue if there is a single point, because lets be
            # real, a single point is silly to plot.
            continue

        polyline = apply_equirectangular_approximation(polyline)
        optional_polyline = custom_scale_polyline(polyline)

        if optional_polyline is not None:
            polylines.append(optional_polyline)

    if not polylines:
        return None

    # To calculate the number of cells in the grid, get the square root of the
    # number of polylines, then round up. If that number is x, we make an x by
    # x grid.
    grid_size = math.ceil(math.sqrt(len(polylines)))

    # Now to calculate the image dimensions, find the largest whole pixel size
    # square, such that a grid of x by x squares (where x was calculated above)
    # including borders.
    square_size = (
        proposed_image_size - ((grid_size + 1) * border_size_px)
    ) // grid_size
    image_size = ((grid_size + 1) * border_size_px) + (grid_size * square_size)

    # Create a white canvas
    width, height = image_size, image_size
    image = img.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    for i, polyline in enumerate(polylines):
        # Calculate col and row from i, then calculate starting position.
        col = i % grid_size
        row = i // grid_size

        starting_x = ((col + 1) * border_size_px) + (square_size * col)
        starting_y = ((row + 1) * border_size_px) + (square_size * row)

        # Scale by the square size
        polyline = [(x * square_size, y * square_size) for (x, y) in polyline]

        # Translate by the starting position.
        polyline = [(x + starting_x, y + starting_y) for (x, y) in polyline]

        # Draw the polylines
        draw.line(
            polyline[0 : int(polyline_fraction * len(polyline))],
            fill="black",
            width=line_thickness,
        )

    return image


def apply_equirectangular_approximation(polyline: Polyline) -> Polyline:
    def equirectangular_approximation(lat, lon, reference_lat):
        R = 6371  # Radius of the Earth in kilometers

        x = R * lon * math.pi / 180 * math.cos(math.radians(reference_lat))
        y = R * lat * math.pi / 180

        return x, y

    polyline = [
        equirectangular_approximation(lat, long, polyline[0][0])
        for (lat, long) in polyline
    ]

    return polyline


def custom_scale_polyline(polyline: Polyline) -> None | Polyline:
    """
    The goal here is to scale some arbitrary polyline into the center of a unit
    square. This will make it easier to place them all in the future.
    """
    # Before we do any scaling, we are going to negate the y axis. This is
    # because Pillow treats the top left at 0,0, and not the bottom left.
    polyline = [(x, -y) for (x, y) in polyline]

    min_x = min(x for (x, y) in polyline)
    min_y = min(y for (x, y) in polyline)
    max_x = max(x for (x, y) in polyline)
    max_y = max(y for (x, y) in polyline)

    # Calculate the dimensions of the bounding box
    width = max_x - min_x
    height = max_y - min_y

    # Handle the case where all points are in the same spot. To avoid a div/0
    # error here, just return None because we can't scale this.
    if max([height, width]) == 0:
        return None

    # Calculate the scaling factors for x and y to fit the polyline into a unit square
    if width > height:
        scaling_factor = 1 / width
    else:
        scaling_factor = 1 / height

    translated_polyline = [(x - min_x, y - min_y) for (x, y) in polyline]

    # Apply the scaling and translation to each point in the polyline
    scaled_polyline = [
        (
            scaling_factor * x,
            scaling_factor * y,
        )
        for (x, y) in translated_polyline
    ]
    return scaled_polyline


def translate_polyline(polyline: Polyline, min_canvas_dimension: int) -> Polyline:
    """
    At this point, the polyline is centered around (0, 0). We want to center it
    in the center of the canvas.
    """
    return [
        (x + (min_canvas_dimension / 2), y + (min_canvas_dimension / 2))
        for (x, y) in polyline
    ]


@dataclasses.dataclass
class CompactActivity:
    type: str
    summary_polyline: str
    start_date_local: dt.datetime


def create_gif_image(
    encoded_polylines: list[str],
    gif_duration_ms: int,
    gif_fps: int,
    proposed_image_size: int = 2000,
    border_size_px: int = 1,
    line_thickness: int = 2,
) -> list[Image]:
    num_frames = int((gif_duration_ms / 1000) * gif_fps)

    return list(
        filter(
            lambda x: x is not None,  # type: ignore
            (
                create_image(
                    encoded_polylines,
                    frame / num_frames,
                    proposed_image_size=proposed_image_size,
                    border_size_px=border_size_px,
                    line_thickness=line_thickness,
                )
                for frame in range(1, num_frames + 1)
            ),
        )
    )


# For testing
if __name__ == "__main__":
    from backend.utils import local_storage

    activity_iterator = local_storage.get_summary_activity_iterator(94896104)
    create_images(activity_iterator, "")
