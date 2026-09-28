/**
 * FitCore Shared Types Foundation
 */

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

export interface HealthCheckResponse {
  status: string;
  service: string;
  environment: string;
  timestamp: string;
  version: string;
}

// User context placeholder for future phases
export interface UserContext {
  id: string;
  email: string;
  name?: string;
}
