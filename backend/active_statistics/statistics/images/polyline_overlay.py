import dataclasses
import json
import math
import os
from typing import Iterator

import polyline
from PIL import Image as img
from PIL import ImageDraw
from PIL.Image import Image
from stravalib.model import Activity

Polyline = list[tuple[float, float]]


def create_images(activity_iterator: Iterator[Activity], path: str) -> None:
    captions: dict[str, str] = {}

    compact_activities = [
        CompactActivity(
            type=activity.type, summary_polyline=activity.map.summary_polyline
        )
        for activity in activity_iterator
    ]
    activity_types = set(
        compact_activity.type for compact_activity in compact_activities
    )

    for activity_type in activity_types:
        image = create_image(
            (
                activity.summary_polyline
                for activity in compact_activities
                if activity.type == activity_type
            ),
            1000,
        )

        if image is None:
            continue

        image_name = f"{activity_type}.png"
        image_path = os.path.join(path, image_name)
        image.save(image_path, "PNG")
        image.close()

        captions[
            image_name
        ] = f"All {activity_type} activities overlaid as if they have the same starting point."

        gif_duration_ms = 3000
        gif_fps = 20
        images = create_gif_image(
            [
                activity.summary_polyline
                for activity in compact_activities
                if activity.type == activity_type
            ],
            gif_duration_ms,
            gif_fps,
        )

        gif_name = f"{activity_type}_animation.gif"
        gif_path = os.path.join(path, gif_name)
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=gif_duration_ms / gif_fps,
            loop=0,
        )
        captions[gif_name] = f"An animation of overlaid {activity_type} activities."

        # Create captions
        # Dump the dictionary to a JSON file
        with open(os.path.join(path, "captions.json"), "w") as json_file:
            json.dump(captions, json_file)


def create_image(
    encoded_polylines: Iterator[str | None],
    image_size: int,
    max_segments_fraction: float = 1.0,
) -> Image | None:
    """
    Creates and returns a PIL image object with all polylines overlaid and
    scaled correctly on top of eachother.

    image_size: the width and height of the image in pixels.

    max_segments_fraction: This is a float between 0 and 1. At 0, nothing is
    plotted. At 0.5, the maximum number of segments allowed to be drawn is 0.5
    * the total number of segments in the polyline with the maximimum number
    of segments. This facilitates the creation of animations.
    """
    polylines: list[Polyline] = []
    for encoded_polyline in encoded_polylines:
        # If the polyline has nothing in it, just return.
        polyline = decode_polyline(encoded_polyline)

        if len(polyline) == 0:
            continue

        polyline = apply_equirectangular_approximation(polyline)
        polyline = transform_to_start_and_end_at_zero(polyline)
        polylines.append(polyline)

    if not polylines:
        return None

    # Create a white canvas
    width = height = image_size
    image = img.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    max_all_max_chebychev_distances = max(
        max_chebychev_distance(polyline) for polyline in polylines
    )

    scaled_polylines = [
        aesthetically_scale_polyline(
            polyline, max_all_max_chebychev_distances, min([height, width])
        )
        for polyline in polylines
    ]

    translated_polylines = [
        translate_polyline(polyline, min([width, height]))
        for polyline in scaled_polylines
    ]

    # Get the number of segments in the polyline with the most segments.
    max_num_polylines = max(len(polyline) for polyline in polylines)

    # Draw the polylines
    for polyline in translated_polylines:
        draw.line(
            polyline[0 : int(max_num_polylines * max_segments_fraction)],
            fill="black",
            width=1,
        )

    return image


def decode_polyline(encoded_polyline: str | None) -> Polyline:
    if encoded_polyline is None:
        return []

    decoded_polyline: Polyline = polyline.decode(encoded_polyline)
    return decoded_polyline


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


def transform_to_start_and_end_at_zero(polyline: Polyline) -> Polyline:
    return [(x - polyline[0][0], y - polyline[0][1]) for (x, y) in polyline]


def max_chebychev_distance(polyline: Polyline) -> float:
    max_x = max(abs(point[0]) for point in polyline)
    max_y = max(abs(point[1]) for point in polyline)
    return max([max_x, max_y])


def aesthetically_scale_polyline(
    polyline: Polyline, max_chebychev_distance: float, min_canvas_dimension: float
) -> Polyline:
    """
    Normalizes the polyline so that all points lie between -1 and 1, while starting at
    Can be multiplied by some scale.
    """

    # 0.5 is because the max chebychev distance in x means that that distance must fit from the center to the edge, not edge to edge.
    # 0.95 is because we don't want to hit the edge of the image for aesthetic purposes.
    polyline = [
        (
            x * ((0.95 * 0.5 * min_canvas_dimension) / max_chebychev_distance),
            y * ((0.95 * 0.5 * min_canvas_dimension) / max_chebychev_distance),
        )
        for (x, y) in polyline
    ]

    # Annoyingly the coordinates of Pillow start at the top left of the screen,
    # so we need to negate y to have things make sense.
    polyline = [(x, -y) for (x, y) in polyline]
    return polyline


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


def create_gif_image(
    encoded_polylines: list[str], gif_duration_ms: int, gif_fps: int
) -> list[Image]:
    num_frames = int((gif_duration_ms / 1000) * gif_fps)

    return list(
        filter(
            (lambda x: x is not None),  # type: ignore
            (
                create_image((_ for _ in encoded_polylines), 1000, frame / num_frames)
                for frame in range(1, num_frames + 1)
            ),
        )
    )


# For testing
if __name__ == "__main__":
    from active_statistics.utils import local_storage

    activity_iterator = local_storage.get_summary_activity_iterator(94896104)
    create_images(activity_iterator, "")
