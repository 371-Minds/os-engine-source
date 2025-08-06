import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  qa_pairs: defineTable({
    question: v.string(),
    answer: v.string(),
    timestamp: v.number(),
    result: v.optional(v.string()),
  }),
  tasks: defineTable({
    body: v.string(),
    isCompleted: v.boolean(),
  }),
});
