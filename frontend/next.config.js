/* Reroute requests to the flask server */

module.exports = () => {
    const rewrites = () => {
        return [
            {
                source: "/api/:path*",
                destination: "http://localhost:5000/api/:path*",
            },
        ];
    };
    return {
        rewrites,
    };
};
