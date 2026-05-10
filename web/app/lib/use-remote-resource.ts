"use client";

import { useEffect, useState } from "react";

export type RemoteResource<T> =
  | { status: "loading"; data: null }
  | { status: "ready"; data: T }
  | { status: "empty"; data: T }
  | { status: "error"; data: null };

export function useRemoteResource<T>(
  load: () => Promise<T>,
  isEmpty: (data: T) => boolean,
): RemoteResource<T> {
  const [resource, setResource] = useState<RemoteResource<T>>({
    status: "loading",
    data: null,
  });

  useEffect(() => {
    let ignore = false;

    async function loadResource() {
      try {
        const data = await load();
        if (!ignore) {
          setResource({ status: isEmpty(data) ? "empty" : "ready", data });
        }
      } catch {
        if (!ignore) {
          setResource({ status: "error", data: null });
        }
      }
    }

    void loadResource();
    return () => {
      ignore = true;
    };
  }, [isEmpty, load]);

  return resource;
}
