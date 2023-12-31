from typing import Iterator

import pandas as pd
import plotly.graph_objects as go
import pytest
from active_statistics.rq_tasks import get_and_process_detailed_statistics
from active_statistics.statistics.images.polyline_grid import create_images
from active_statistics.statistics.trivia.trivia import TriviaProcessor
from active_statistics.tabs.image_tab import ImageTab
from active_statistics.tabs.plot_tabs import PlotTab
from active_statistics.tabs.table_tab import TableTab
from active_statistics.tabs.tabs import Tab
from active_statistics.tabs.trivia_tabs import TriviaTab
from pytest import MonkeyPatch
from stravalib.model import Activity, Map
from tests.factories.activity_factories import ActivityFactory


class TestProcessingTabs:
    @pytest.fixture
    def mock_most_functions(self, monkeypatch) -> None:
        # Define mock functions that do nothing
        def mock_get_client_for_athlete(athlete_id, rate_limiter=None):
            pass

        def mock_get_and_save_detailed_activities(
            client, athlete_id, activities: list[Activity]
        ):
            return [
                ActivityFactory(
                    map=Map(
                        id="1",
                        summary_polyline="loufDye~d\\j@EfAu@t@m@rBeCf@a@dAa@`@If@O`AUdCqA`@Mb@D`@Gb@UHGN]RyAPW~@i@ZGHBh@v@Pd@RLLAPMY{@Se@o@}@Y[USaAs@_B}@kAw@a@i@i@_AaBsBiAa@IKCm@M]m@u@eA{@Yc@EUIMKGGOc@]AE@ED?B@HPLd@bAbAl@x@TNl@f@\\n@Fb@|@j@fBfCz@rA`ChA^Tp@h@l@^`@`@d@v@dAfC?HMHS@KESQQa@SW]IKA_@Bg@TGJKp@El@GT]d@k@Nm@?e@Bc@Ve@PgEhAi@Ro@`@s@h@]d@Wb@iAnAqAv@{AbA_Bt@cB~@[b@yBhAuC|B_@Xm@\\c@^e@Za@PK@_@?sBjAa@XuAt@u@^_Ap@gAd@Ol@Ud@g@f@Yb@Ud@IJE@Qf@Jf@jAfBa@_@w@iAIe@Ne@p@}AnAyAVe@rA{@b@c@hDoBjCeBZ@`@Gb@Oj@c@rAy@LO^[lBkAr@]^Y\\m@j@_@jCoA`@]Zi@DA",
                    )
                )
            ]

        def mock_get_summary_activities(client, athlete_id: int) -> list[Activity]:
            return [ActivityFactory()]

        # Monkeypatch the functions in the rq_tasks module
        monkeypatch.setattr(
            "active_statistics.rq_tasks.get_client_for_athlete",
            mock_get_client_for_athlete,
        )
        monkeypatch.setattr(
            "active_statistics.rq_tasks.get_and_save_detailed_activities",
            mock_get_and_save_detailed_activities,
        )
        monkeypatch.setattr(
            "active_statistics.rq_tasks.get_summary_activities",
            mock_get_summary_activities,
        )

    def test_process_plot_tab(self, mock_most_functions, monkeypatch: MonkeyPatch):
        def mock_get_all_tabs() -> list[Tab]:
            return [
                PlotTab(
                    "Test Plot Tab",
                    detailed=True,
                    description="",
                    plot_function=test_plot_function,
                )
            ]

        def test_plot_function(activities: Iterator[Activity]) -> go.Figure:
            return go.Figure()

        monkeypatch.setattr(
            "active_statistics.rq_tasks.get_all_tabs", mock_get_all_tabs
        )

        get_and_process_detailed_statistics(1)

    def test_process_trivia_tab(self, mock_most_functions, monkeypatch: MonkeyPatch):
        def mock_get_all_tabs() -> list[Tab]:
            trivia_processor = TriviaProcessor()
            return [
                TriviaTab(
                    "Test Plot Tab",
                    detailed=True,
                    description="",
                    trivia_processor=trivia_processor,
                )
            ]

        monkeypatch.setattr(
            "active_statistics.rq_tasks.get_all_tabs", mock_get_all_tabs
        )

        get_and_process_detailed_statistics(1)

    def test_process_table_tab(self, mock_most_functions, monkeypatch: MonkeyPatch):
        def mock_get_all_tabs() -> list[Tab]:
            def table_function(activities: Iterator[Activity]) -> pd.DataFrame:
                return pd.DataFrame()

            return [
                TableTab(
                    "Test Plot Tab",
                    detailed=True,
                    description="",
                    table_function=table_function,
                )
            ]

        monkeypatch.setattr(
            "active_statistics.rq_tasks.get_all_tabs", mock_get_all_tabs
        )

        get_and_process_detailed_statistics(1)

    def test_process_image_tab(self, mock_most_functions, monkeypatch: MonkeyPatch):
        def mock_get_all_tabs() -> list[Tab]:
            return [
                ImageTab(
                    "Test Plot Tab",
                    detailed=True,
                    description="",
                    create_images_function=create_images,
                )
            ]

        monkeypatch.setattr(
            "active_statistics.rq_tasks.get_all_tabs", mock_get_all_tabs
        )

        get_and_process_detailed_statistics(1)
