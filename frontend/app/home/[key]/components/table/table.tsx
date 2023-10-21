import Link from "next/link";

export default function Table({
  table_data,
  show_headings,
  column_info,
}: {
  table_data: { [key: string]: any[] };
  show_headings: boolean;
  column_info: { column_name: string; column_type: string }[];
}) {
  return (
    <>
      <table className="bg-green-500 table-auto border-separate border-spacing-1 text-sm rounded-lg sm:text-base sm:border-spacing-2 h-max">
        <thead>
          {show_headings && <tr>{column_info.map((column) => get_headings(column))}</tr>}
        </thead>
        <tbody>
          {table_data[column_info[0].column_name].map((_, index) =>
            get_row(index, table_data, column_info)
          )}
        </tbody>
      </table>
    </>
  );
}

function get_headings(column: { column_name: string; column_type: string }) {
  return <th key={column.column_name}>{column.column_name}</th>;
}

function get_row(
  index: number,
  table_data: { [key: string]: any[] },
  column_info: { column_name: string; column_type: string }[]
) {
  return (
    <tr className="bg-green-400 hover:bg-green-600" key={index}>
      {column_info.map((column) => (
        <td className="p-1 sm:p-2 rounded-lg" key={column.column_name}>
          {get_cell(table_data[column.column_name][index], column.column_type)}
        </td>
      ))}
    </tr>
  );
}

function get_cell(data: any, cell_type: string) {
  if (cell_type == "string") {
    return data;
  }

  if (cell_type == "link") {
    if (data == null) {
      return null;
    }

    return (
      <Link className="hyperlink" href={data.url}>
        {data.text}
      </Link>
    );
  }

  throw new Error("Unknown cell type received.");
}
