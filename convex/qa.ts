import { query, mutation, action } from "./_generated/server";
import { v } from "convex/values";
import { api } from "./_generated/api";

export const ask = mutation({
  args: {
    question: v.string(),
  },
  handler: async (ctx, args) => {
    const questionId = await ctx.db.insert("qa_pairs", {
      question: args.question,
      answer: "...",
      timestamp: Date.now(),
    });

    await ctx.scheduler.runAfter(0, api.qa.getAnswer, { questionId, question: args.question });

    return questionId;
  },
});

export const getAnswer = action({
  args: {
    questionId: v.id("qa_pairs"),
    question: v.string(),
  },
  handler: async (ctx, args) => {
    const answer = await ctx.runAction(api.http.callAgent, { task: args.question });
    await ctx.runMutation(api.qa.updateAnswer, {
      questionId: args.questionId,
      answer: await answer.json(),
    });
  },
});

export const updateAnswer = mutation({
  args: {
    questionId: v.id("qa_pairs"),
    answer: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.questionId, { answer: args.answer });
  },
});

export const getHistory = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("qa_pairs").order("desc").collect();
  },
});
