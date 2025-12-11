export default async function handler(req, res) {
  const token = process.env.MY_GITHUB_TOKEN; 
  
  const user = "Ch4Angelia";
  const repo = "computerscience";
  const eventType = "trigger_update";

  if (!token) {
    return res.status(500).json({ error: "Server Error: Token not found." });
  }

  try {
    const response = await fetch(`https://api.github.com/repos/${user}/${repo}/dispatches`, {
      method: 'POST',
      headers: {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': `token ${token}`,
        'User-Agent': 'Vercel-Serverless-Function'
      },
      body: JSON.stringify({ event_type: eventType })
    });

    if (response.ok) {
      return res.status(200).json({ message: "Update triggered successfully!" });
    } else {
      const errorText = await response.text();
      return res.status(response.status).json({ error: "GitHub API Error", details: errorText });
    }
  } catch (error) {
    return res.status(500).json({ error: "Internal Server Error", details: error.message });
  }
}