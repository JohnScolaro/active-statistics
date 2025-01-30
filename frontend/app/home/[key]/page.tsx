import PageClient from "./components/page_client";
import { use } from 'react'

type Params = Promise<{ key: string }>
type SearchParams = Promise<{ [key: string]: string | string[] | undefined }>

export default function Page(props: {
  params: Params
  searchParams: SearchParams
}) {
  return (<PageClient params={use(props.params)}></PageClient>)
}

export async function generateStaticParams() {
  return [
    // Plots
    { key: 'cumulative_time' },
    { key: 'cumulative_distance' },
    { key: 'cumulative_elevation' },
    { key: 'cumulative_kudos' },
    { key: 'calendar' },
    { key: 'average_hr_by_average_speed' },
    { key: 'pace_timeline' },
    { key: 'histogram_of_activity_times' },
    // Tables
    { key: 'min_and_max_distance_activities' },
    { key: 'min_and_max_elevation_activities' },
    { key: 'general_trivia' },
    { key: 'flagged_activities' },
    { key: 'top_100_longest_runs' },
    { key: 'top_100_longest_rides' },
    // Images
    { key: 'polyline_grid' },
    { key: 'animated_polyline_grid' },
  ];
}