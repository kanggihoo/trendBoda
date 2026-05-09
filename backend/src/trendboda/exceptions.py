class TrendBodaError(Exception):
    status_code = 500
    code = "internal_server_error"
    public_message = "Internal server error"


class GeekNewsFetchFailed(TrendBodaError):
    status_code = 502
    code = "geeknews_fetch_failed"
    public_message = "GeekNews fetch failed"
