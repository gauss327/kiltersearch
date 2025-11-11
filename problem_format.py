{
  "id": "route_0001",
  "name": "Problem Name",
  "keywords": ["spanny", "tension", "few holds"],

  "metadata": {
    "grade": "V5",
    "setter": "Setter Name",

  },

  "board": {
    "width_cols": 20,
    "height_rows": 35,
    "angle_deg": 40
  },

  "holds": [
    {
      "coordinate": "16,5",
      "x": 64,
      "y": 32,
      "role": "start",           // one of: start|middle|finish|foot
      "description": "jug start"
    }
    // ... more holds
  ],

  "metrics": {
    "number_handholds": 5,
    "number_footholds": 3,
    "hold_density": 0.12,

  },

  "labels": {
    "span": "high",               // low|medium|high|very_high
    "max_move": "very_high",
    "spread": "medium",
    "sparsity": "high",
    "feet_density": "low",
    "intensity": "high"
  },

  "style": {
    "style_tags": ["crimp", "sloper", "undercling"],
    "notes": ["scarce feet mid-route", "one big rightward bump"],
    "feet_context": "kickboard_only_start"
  },


  "summary": "Reachy set with one very big move (~0.39 of the board diagonal) and generally high spacing. Scarce feet create body tension through the middle; mix of crimps and a usable sloper up high.",

  "embedding": {
    "fused_text": "[TAGS] SPAN=HIGH MAXMOVE=VERY_HIGH P90MOVE=HIGH SPREAD_HULL=0.31 RADIUS=0.44 HOLDS=7 STEEPNESS=40D STYLE=SLOPER,CRIMP,UNDERCLING FEET_DENSITY=LOW\nsynonyms: spanny reachy long-reach big move tension burly thuggy sparse few holds techy scrunchy\nsummary: Reachy set with one very big move (~0.39 of the board diagonal) and generally high spacing. Scarce feet create body tension through the middle; mix of crimps and a usable sloper up high.",
    "control_text": "[TAGS] SPAN=HIGH MAXMOVE=VERY_HIGH P90MOVE=HIGH SPREAD_HULL=0.31 RADIUS=0.44 HOLDS=7 STEEPNESS=40D STYLE=SLOPER,CRIMP,UNDERCLING FEET_DENSITY=LOW",
    "semantic_text": "Reachy with a very big move and scarce feet causing tension; crimps and a positive sloper near the top."
  },

}





