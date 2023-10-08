export function getUrl(endpoint: string = ''): string {
    const protocol: string = process.env.PROTOCOL || 'http';
    const domain: string = process.env.DOMAIN || 'localhost';
    const port: string = process.env.PORT || '3000';

    const baseUrl: string = `${protocol}://${domain}:${port}`;

    return endpoint ? `${baseUrl}/${endpoint}` : baseUrl;
}
