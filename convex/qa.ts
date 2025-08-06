import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const ask = mutation({
  args: {
    question: v.string(),
  },
  handler: async (ctx, args) => {
    const answer = "This is a dummy answer from the Convex backend.";
    await ctx.db.insert("qa_pairs", {
      question: args.question,
      answer: answer,
      timestamp: Date.now(),
    });
    return answer;
  },
});

export const getHistory = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("qa_pairs").order("desc").collect();
  },
});
