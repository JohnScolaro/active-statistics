

export default function Page({ params }: { params: { key: string } }) {
    return <div>Content key: {params.key}</div>
}
