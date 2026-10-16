export type Affects = {
    lines: string[];
    stops: string[];
    journeys: string[];
};

export type Alert = {
    id: string;
    creation_time: string | null;
    status: string | null;
    severity: string | null;
    start_time: string | null;
    end_time: string | null;
    summary: string | null;
    description: string | null;
    affects: Affects;
};