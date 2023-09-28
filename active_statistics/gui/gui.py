from active_statistics.gui.plot_tabs import PlotTab
from active_statistics.gui.table_tab import TableTab
from active_statistics.gui.tabs import Tab
from active_statistics.gui.trivia_tabs import TriviaTab
from active_statistics.statistics.plots import (
    average_heartrate_by_average_speed,
    cumulative_distance_travelled,
    cumulative_gear_distance,
    cumulative_gear_time,
    cumulative_time_spent,
    github_style_activities,
    histogram_of_activity_time,
    pace_timeline,
    personal_bests,
)
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

all_tabs: list[Tab] = [
    PlotTab(
        name="Cumulative Time",
        description="A cumulative plot of how much time you've logged on Strava for each of your activity types.",
        plot_function=cumulative_time_spent.plot,
        detailed=False,
    ),
    PlotTab(
        name="Cumulative Distance",
        description="A cumulative plot of the total distance you've travelled from the activities that you've logged on Strava.",
        plot_function=cumulative_distance_travelled.plot,
        detailed=False,
    ),
    PlotTab(
        name="Calendar",
        description="This plot draws inspiration from the GitHub contributions plot to show how much you're running over a calendar year.",
        plot_function=github_style_activities.plot,
        detailed=False,
    ),
    PlotTab(
        name="Average HR by Average Speed",
        description="This plot shows your average heartrate by your average speed for all running activities. It needs activities with an average heartrate to work, so if you don't record your heartrate with your activities, then this plot will be blank.",
        plot_function=average_heartrate_by_average_speed.plot,
        detailed=False,
    ),
    PlotTab(
        name="Pace Timeline",
        description="This plot shows the pace of your runs on a timeline. Overlaid, there is a 30 day moving average line. At any point on this line, the value is the average pace of all runs 15 days in front and behind it.",
        plot_function=pace_timeline.plot,
        detailed=False,
    ),
    PlotTab(
        name="Histogram of Activity Times",
        description="This is a histogram of all your activity start times.",
        plot_function=histogram_of_activity_time.plot,
        detailed=False,
    ),
    TriviaTab(
        name="Min and Max Distance Activities",
        detailed=False,
        description="Some Trivia about your longest and shortest Strava activities.",
        trivia_processor=min_and_max_distance_trivia_processor,
    ),
    TriviaTab(
        name="Min and Max Elevation Activities",
        detailed=False,
        description="Some Trivia about your hilliest and flattest Strava activities.",
        trivia_processor=min_and_max_elevation_trivia_processor,
    ),
    TriviaTab(
        name="General Trivia",
        detailed=False,
        description="Some miscellaneous trivia about your Strava activities.",
        trivia_processor=general_trivia,
    ),
    TableTab(
        name="Flagged Activities",
        detailed=False,
        description="If any of your activities have been flagged for cheating on Strava, they will be displayed in a table below.",
        table_function=flagged_activities_table,
    ),
    PlotTab(
        name="Personal Bests",
        description='This is a chart that shows a timeline of your personal bests. It is calculated using Strava\'s "Best Efforts" from all of your activities.',
        plot_function=personal_bests.plot,
        detailed=True,
    ),
    PlotTab(
        name="Cumulative Gear Time",
        description="A cumulative plot of the time logged with Strava using different gear.",
        plot_function=cumulative_gear_time.plot,
        detailed=True,
    ),
    PlotTab(
        name="Cumulative Gear Distance",
        description="A cumuative plot of the distance travelled while using different gear that you've logged on Strava.",
        plot_function=cumulative_gear_distance.plot,
        detailed=True,
    ),
    TriviaTab(
        name="Detailed Trivia",
        detailed=True,
        description="Some more in-depth trivia about your Strava activities, which requires downloading your detailed activities to see.",
        trivia_processor=detailed_trivia_processor,
    ),
]
