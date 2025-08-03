import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

export const add = mutation({
  args: {
    body: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.insert("tasks", {
      body: args.body,
      isCompleted: false,
    });
  },
});
