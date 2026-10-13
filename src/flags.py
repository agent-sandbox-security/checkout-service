ENABLED = {
    "new_cart_ui": True,
    "express_checkout": True,
    "loyalty_points_v2": True,
}

# Forced off during incident (issue #31): promo_engine_v3 rollout caused 500s.
FORCE_OFF = {"promo_engine_v3"}

def is_enabled(flag):
    if flag in FORCE_OFF:
        return False
    return ENABLED.get(flag, False)
