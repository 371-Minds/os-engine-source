import { httpAction } from "./_generated/server";

export const callAgent = httpAction(
  async (_, request) => {
    const { task } = await request.json();

    const response = await fetch("http://localhost:8000/api/agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task }),
    });

    if (!response.ok) {
      throw new Error(`Agent request failed with status ${response.status}`);
    }

    return response;
  },
);
