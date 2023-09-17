stage_configuration = {
    "stage_1": {
        "waves": [
            {
                "wave_number": 0,
                "enemy_count": 1,
                "vehicle_count": 9,
                "enemy_types": ["advanced"],
                "vehicle_types": ["car"],
                "cooldown": 5
            },
            {
                "wave_number": 1,
                "enemy_count": 2,
                "vehicle_count": 2,
                "enemy_types": ["advanced"],
                "vehicle_types": ["car", "scooter"],
                "cooldown": 5
            },
            {
                "wave_number": 2,
                "enemy_count": 3,
                "vehicle_count": 7,
                "enemy_types": ["advanced"],
                "vehicle_types": ["car", "scooter"],
                "cooldown": 8
            },
            {
                "wave_number": 3,
                "enemy_count": 4,
                "vehicle_count": 12,
                "enemy_types": ["advanced"],
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
