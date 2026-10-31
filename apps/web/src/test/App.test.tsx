
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import App from '../App';

describe('Yatranook application', () => {
  it('renders the landing page', () => {
    window.history.pushState({}, '', '/');

    render(<App />);

    expect(
      screen.getByText(/your journey,/i),
    ).toBeInTheDocument();

    const planTripLinks = screen.getAllByRole('link', {
      name: /plan a trip/i,
    });

    expect(planTripLinks.length).toBeGreaterThan(0);
  });
});
