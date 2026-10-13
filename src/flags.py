# Feature flags evaluated at request time. To force a flag off during an
# incident, add it to FORCE_OFF.
ENABLED = {
    "new_cart_ui": True,
    "express_checkout": True,
    "loyalty_points_v2": True,
}

FORCE_OFF: set[str] = {
    "promo_engine_v3",  # causing NoneType_in_apply_promo 500s since 2026-10-07 07:31
}

def is_enabled(flag):
    if flag in FORCE_OFF:
        return False
    return ENABLED.get(flag, False)
