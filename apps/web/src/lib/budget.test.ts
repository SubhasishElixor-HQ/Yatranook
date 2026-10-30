import { describe, expect, it } from 'vitest';
import { validateBudgetInput } from './budget';

describe('validateBudgetInput', () => {
  it('accepts a small positive budget', () => {
    expect(validateBudgetInput('50')).toEqual({ valid: true, amount: 50 });
  });
  it('rejects empty, zero, negative and non-numeric values', () => {
    expect(validateBudgetInput(' ').valid).toBe(false);
    expect(validateBudgetInput('0').valid).toBe(false);
    expect(validateBudgetInput('-20').valid).toBe(false);
    expect(validateBudgetInput('abc').valid).toBe(false);
  });
});
