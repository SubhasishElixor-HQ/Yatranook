export type BudgetValidation = { valid: true; amount: number } | { valid: false; message: string };

/** A positive low budget is valid input; feasibility is evaluated separately by the planner. */
export function validateBudgetInput(raw: string): BudgetValidation {
  if (!raw.trim()) return { valid: false, message: 'Enter a budget amount.' };
  const amount = Number(raw);
  if (!Number.isFinite(amount) || amount <= 0) return { valid: false, message: 'Enter a valid positive amount.' };
  return { valid: true, amount };
}
