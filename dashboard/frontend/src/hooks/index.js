import { useAsync } from "./useAsync";
import api from "../api/client";

export function usePrices({ start, end, resample } = {}) {
  return useAsync(() => api.prices({ start, end, resample }), [start, end, resample]);
}

export function useEvents({ category, start, end } = {}) {
  return useAsync(() => api.events({ category, start, end }), [category, start, end]);
}

export function useEventCategories() {
  return useAsync(() => api.eventCategories(), []);
}

export function useChangePoints() {
  return useAsync(() => api.changePoints(), []);
}

export function useRegimes() {
  return useAsync(() => api.regimes(), []);
}

export function useMetrics() {
  return useAsync(() => api.metrics(), []);
}
