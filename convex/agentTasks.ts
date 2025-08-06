import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const addAgentTask = mutation({
  args: {
    task: v.string(),
  },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      body: args.task,
      isCompleted: false,
    });
    return taskId;
  },
});

export const getAgentTask = query({
  args: {
    taskId: v.id("tasks"),
  },
  handler: async (ctx, args) => {
    const task = await ctx.db.get(args.taskId);
    return task;
  },
});
