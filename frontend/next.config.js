/* Reroute requests to the flask server */

module.exports = () => {
    const rewrites = () => {
        return [
            {
                source: "/:path*",
                destination: "http://localhost:5000/:path*",
            },
        ];
    };
    return {
        rewrites,
    };
};
