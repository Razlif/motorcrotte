stage_configuration = {
    "stage_1": {
        "waves": [
            {
                "wave_number": 0,
                "enemy_count": 1,
                "vehicle_count": 5,
                "enemy_types": ["simple"],
                "vehicle_types": ["car", "scooter"],
                "cooldown": 5
            },
            {
                "wave_number": 1,
                "enemy_count": 2,
                "vehicle_count": 5,
                "enemy_types": ["simple", "advanced"],
                "vehicle_types": ["car", "scooter"],
                "cooldown": 5
            },
            {
                "wave_number": 2,
                "enemy_count": 3,
                "vehicle_count": 8,
                "enemy_types": ["simple", "advanced"],
                "vehicle_types": ["car", "scooter"],
                "cooldown": 8
            },
            {
                "wave_number": 3,
                "enemy_count": 5,
                "vehicle_count": 2,
                "enemy_types": ["simple", "advanced"],
                "vehicle_types": ["car", "scooter"],
                "cooldown": 8
            },
            {
                "wave_number": 4,
                "enemy_count": 1,
                "vehicle_count": 0,
                "enemy_types": ["boss"],
                "vehicle_types": ["car", "scooter"],
                "cooldown": 8
            },
            # More waves can be added here
        ],
    },
    # More stages can be added here
}
