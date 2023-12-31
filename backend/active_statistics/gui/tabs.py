from active_statistics.statistics.images import polyline_grid, polyline_overlay
from active_statistics.statistics.plots import (
    average_heartrate_by_average_speed,
    cumulative_anything,
    cumulative_gear_distance,
    cumulative_gear_time,
    github_style_activities,
    histogram_of_activity_time,
    pace_timeline,
    personal_bests,
)
from active_statistics.statistics.tables import top_hundred
from active_statistics.statistics.tables.flagged_activities import (
    flagged_activities_table,
)
from active_statistics.statistics.trivia.detailed_trivia import (
    detailed_trivia_processor,
)
from active_statistics.statistics.trivia.min_max_summary_trivia import (
    min_and_max_distance_trivia_processor,
    min_and_max_elevation_trivia_processor,
)
from active_statistics.statistics.trivia.summary_trivia import general_trivia
from active_statistics.tabs.image_tab import ImageTab
from active_statistics.tabs.plot_tabs import PlotTab
from active_statistics.tabs.table_tab import TableTab
from active_statistics.tabs.trivia_tabs import TriviaTab

cumulative_time_tab = PlotTab(
    name="Cumulative Time",
    description="A cumulative plot of how much time you've logged on Strava for each of your activity types.",
    plot_function=cumulative_anything.get_plot_function(
        "moving_time",
        cumulative_anything.conversion_function_for_timedeltas,
        "Hours",
        cumulative_anything.get_title_for_cumulative_time_plot,
    ),
    detailed=False,
)

cumulative_distance_tab = PlotTab(
    name="Cumulative Distance",
    description="A cumulative plot of the total distance you've travelled from the activities that you've logged on Strava.",
    plot_function=cumulative_anything.get_plot_function(
        "distance",
        cumulative_anything.conversion_function_for_distance_to_km,
        "Kilometers",
        cumulative_anything.get_title_for_cumulative_distance_plot,
    ),
    detailed=False,
)

cumulative_elevation_tab = PlotTab(
    name="Cumulative Elevation",
    description="A cumulative plot of the total elevation you've climbed from the activities that you've logged on Strava.",
    plot_function=cumulative_anything.get_plot_function(
        "total_elevation_gain",
        cumulative_anything.conversion_function_for_distance_to_m,
        "Meters",
        cumulative_anything.get_title_for_cumulative_elevation_plot,
    ),
    detailed=False,
)

cumulative_kudos_tab = PlotTab(
    name="Cumulative Kudos",
    description="A cumulative plot of the total kudos you've received each year.",
    plot_function=cumulative_anything.get_plot_function(
        "kudos_count",
        cumulative_anything.conversion_function_for_int,
        "Kudos",
        cumulative_anything.get_title_for_cumulative_kudos_plot,
    ),
    detailed=False,
)


calendar_tab = PlotTab(
    name="Calendar",
    description="This plot draws inspiration from the GitHub contributions plot to show how much you're running over a calendar year.",
    plot_function=github_style_activities.plot,
    detailed=False,
)

average_hr_by_average_speed_tab = PlotTab(
    name="Average HR by Average Speed",
    description="This plot shows your average heartrate by your average speed for all running activities. It needs activities with an average heartrate to work, so if you don't record your heartrate with your activities, then this plot will be blank.",
    plot_function=average_heartrate_by_average_speed.plot,
    detailed=False,
)

pace_timeline_tab = PlotTab(
    name="Pace Timeline",
    description="This plot shows the pace of your runs on a timeline. Overlaid, there is a 30 day moving average line. At any point on this line, the value is the average pace of all runs 15 days in front and behind it.",
    plot_function=pace_timeline.plot,
    detailed=False,
)

histogram_of_activity_times_tab = PlotTab(
    name="Histogram of Activity Times",
    description="This is a histogram of all your activity start times.",
    plot_function=histogram_of_activity_time.plot,
    detailed=False,
)

min_and_max_distance_activities_tab = TriviaTab(
    name="Min and Max Distance Activities",
    detailed=False,
    description="Some Trivia about your longest and shortest Strava activities.",
    trivia_processor=min_and_max_distance_trivia_processor,
)

min_and_max_elevation_activities_tab = TriviaTab(
    name="Min and Max Elevation Activities",
    detailed=False,
    description="Some Trivia about your hilliest and flattest Strava activities.",
    trivia_processor=min_and_max_elevation_trivia_processor,
)

general_trivia_tab = TriviaTab(
    name="General Trivia",
    detailed=False,
    description="Some miscellaneous trivia about your Strava activities.",
    trivia_processor=general_trivia,
)

flagged_activities_tab = TableTab(
    name="Flagged Activities",
    detailed=False,
    description="If any of your activities have been flagged for cheating on Strava, they will be displayed in a table below.",
    table_function=flagged_activities_table,
)

top_100_longest_runs_tab = TableTab(
    name="Top 100 Longest Runs",
    description="Shows the top 100 longest runs you've ever done.",
    table_function=top_hundred.get_top_hundred_table_function(
        "Run",
        "distance",
        "Distance (km)",
        top_hundred.distance_conversion_function_to_km,
    ),
    detailed=False,
)

top_100_longest_rides_tab = TableTab(
    name="Top 100 Longest Rides",
    description="Shows the top 100 longest rides you've ever done.",
    table_function=top_hundred.get_top_hundred_table_function(
        "Ride",
        "distance",
        "Distance (km)",
        top_hundred.distance_conversion_function_to_km,
    ),
    detailed=False,
)

polyline_overlay_tab = ImageTab(
    name="Polyline Overlay",
    detailed=False,
    description="yeet",
    create_images_function=polyline_overlay.create_images,
)

polyline_grid_tab = ImageTab(
    name="Polyline Grid",
    detailed=False,
    description="yeet",
    create_images_function=polyline_grid.create_images,
)

personal_bests_tab = PlotTab(
    name="Personal Bests",
    description='This is a chart that shows a timeline of your personal bests. It is calculated using Strava\'s "Best Efforts" from all of your activities.',
    plot_function=personal_bests.plot,
    detailed=True,
)

cumulative_gear_time_tab = PlotTab(
    name="Cumulative Gear Time",
    description="A cumulative plot of the time logged with Strava using different gear.",
    plot_function=cumulative_gear_time.plot,
    detailed=True,
)

cumulative_gear_distance_tab = PlotTab(
    name="Cumulative Gear Distance",
    description="A cumuative plot of the distance travelled while using different gear that you've logged on Strava.",
    plot_function=cumulative_gear_distance.plot,
    detailed=True,
)

detailed_trivia_tab = TriviaTab(
    name="Detailed Trivia",
    detailed=True,
    description="Some more in-depth trivia about your Strava activities, which requires downloading your detailed activities to see.",
    trivia_processor=detailed_trivia_processor,
)
