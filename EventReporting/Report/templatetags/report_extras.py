from django import template

register = template.Library()


@register.filter
def split_commas(value):
    """'a,b,c' -> ['a', 'b', 'c'] — used to render option lists in templates."""
    return [v.strip() for v in str(value).split(",") if v.strip()]


@register.filter
def type_badge(value):
    """Map an event type to a badge CSS class."""
    return {
        "Near Miss": "badge-nearmiss",
        "Unsafe Condition": "badge-unsafe",
        "Process Improvement": "badge-process",
        "Therapuetic radiation incident": "badge-radiation",
        "Other safety incident": "badge-other",
    }.get(value, "badge-default")


@register.filter
def type_short(value):
    """Shorter display label for an event type, used in the list view."""
    return {
        "Therapuetic radiation incident": "Radiation Incident",
        "Other safety incident": "Other Safety Incident",
    }.get(value, value)
