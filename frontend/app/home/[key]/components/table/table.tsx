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
  console.log(column_info);
  return (
    <>
      <table className="bg-slate-500 m-2 p-2">
        <thead className="bg-slate-600 m-2 p-2">
          {show_headings && (
            <tr className="bg-green-900 p-2 m-2">
              {column_info.map((column) => get_headings(column))}
            </tr>
          )}
        </thead>
        <tbody className="bg-slate-700 m-2 p-2">
          {table_data[column_info[0].column_name].map((_, index) =>
            get_row(index, table_data, column_info)
          )}
        </tbody>
      </table>
    </>
  );
}

function get_headings(column: { column_name: string; column_type: string }) {
  console.log(column);
  return (
    <th className="bg-red-600 p-2" key={column.column_name}>
      {column.column_name}
    </th>
  );
}

function get_row(
  index: number,
  table_data: { [key: string]: any[] },
  column_info: { column_name: string; column_type: string }[]
) {
  console.log(index);
  console.log(table_data);

  return (
    <tr className="bg-red-700 p-2 m-2" key={index}>
      {column_info.map((column) => (
        <td className="bg-red-800 p-2 m-2" key={column.column_name}>
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

    return <Link href={data.url}>{data.text}</Link>;
  }

  throw new Error("Unknown cell type received.");
}
