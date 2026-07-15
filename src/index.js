export default {
  async fetch(request, env) {
    const authHeader = request.headers.get("Authorization");

    if (authHeader) {
      const [scheme, encoded] = authHeader.split(" ");
      if (scheme === "Basic" && encoded) {
        const decoded = atob(encoded);
        const colonIndex = decoded.indexOf(":");
        if (colonIndex !== -1) {
          const username = decoded.slice(0, colonIndex);
          const password = decoded.slice(colonIndex + 1);
          if (username === env.JUDGE_USERNAME && password === env.JUDGE_PASSWORD) {
            return env.ASSETS.fetch(request);
          }
        }
      }
    }

    return new Response("Authentication required", {
      status: 401,
      headers: {
        "WWW-Authenticate": 'Basic realm="Sparkathon Judge Login"',
      },
    });
  },
};
