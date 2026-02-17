COLORS = {
    # --- Brand ---
    "primary":          "#004D40",
    "primary_600":      "#00332B",
    "primary_300":      "#2A7D72",
    "accent":           "#00C853",
    "accent_700":       "#00A63F",

    # --- Backgrounds ---
    "bg":               "#0B1214",
    "surface":          "#102022",
    "surface_variant":  "#0E1A1C",

    # --- Text ---
    "text_primary":     "#E6F7EF",
    "text_secondary":   "#8AA39A",

    # --- Semantic ---
    "info":             "#00E5FF",
    "success":          "#00C853",
    "danger":           "#E74C3C",
    "border":           "#183233",

    # --- Glows (active states / CTAs only) ---
    "glow_cyan":        "rgba(0,229,255,0.08)",
    "glow_green":       "rgba(0,200,83,0.18)",
}


def style(**kwargs):
    """Build an inline style dict. Accepts color token names as values.

    Example:
        style(backgroundColor="surface", color="text_primary")
        style(backgroundColor="#102022", color="#E6F7EF")  # raw hex also fine
    """
    return {k: COLORS.get(v, v) for k, v in kwargs.items()}
