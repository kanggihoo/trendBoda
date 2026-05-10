class TrendBodaError(Exception):
    status_code = 500
    code = "internal_server_error"
    public_message = "Internal server error"


class GeekNewsFetchFailed(TrendBodaError):
    status_code = 502
    code = "geeknews_fetch_failed"
    public_message = "GeekNews fetch failed"


class GeekNewsItemNotFound(TrendBodaError):
    status_code = 404
    code = "geeknews_item_not_found"
    public_message = "GeekNews item not found"


class GeekNewsSummaryFailed(TrendBodaError):
    status_code = 502
    code = "geeknews_summary_failed"
    public_message = "GeekNews summary failed"
