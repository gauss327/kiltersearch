"""
Definitions of hold orientations and their detailed descriptions.
This file serves as a single source of truth for hold orientation types and hold types.
"""

ORIENTATION_MAPPINGS = {
    "upright": {
        "description": "Arm approaches hold vertically. Most intuitive type of hold. Palm is facing down when holding."
    },
    "tilted left": {
        "description": "Hold is oriented towards the left. Left hand can approach the hold straight on. Right hand would likely be a gaston."
    },
    "left": {
        "description": "Hold is tilted 90 degrees directly to the left. For side pulls or aggressive gastons. "
    },
    "tilted right": {
        "description": "Hold is oriented towards the right. Right hand can approach the hold straight on. Left hand would likely be a gaston"
    },
    "right": {
        "description": "Hold is tilted 90 degrees directly to the right. For side pulls or aggressive gastons. "
    },
    "downright": {
        "description": "Hold is upside down. This will likely be used as an undercling. These holds often require a good amount of body tension with footholds to stay on the wall."
    },
    "heavy right": {
        "description": "Hold is tilted 135 degrees to the right. Mainly used as an undercling, with palm facing up when holding."
    },
    "heavy left": {
        "description": "Hold is tilted 135 degrees to the left. Mainly used as an undercling, with palm facing up when holding."
    },
    "pinch upright": {
        "description": "Pinch is directly vertical. Hardest type of pinch to hold as difficult to use body tension to make hold easier."
    },
    "pinch left": {
        "description": "Pinch is tilted towards the left. Makes holding it with the left hand more natural. Would be a right hand gaston or potentially even an undercling."
    },
    "pinch right": {
        "description": "Pinch is tilted towards the right. Makes holding it with the right hand more natural. Would be a left hand gaston or potentially even an undercling."
    },
    "misc": {
        "description": "No specific orientation of hold"
    }
}

HOLD_TYPES = {
    "jug": {
        "description": "Large, positive hold that can be gripped with the whole hand",
    },
    "crimp": {
        "description": "Small edge that can only be gripped with the fingertips",
    },
    "pinch": {
        "description": "Hold that requires pinching between thumb and fingers",
    },
    "sloper": {
        "description": "Rounded hold with no positive edge, requires friction and body tension",
    },
    "foot": {
        "description": "Hold designed for foot placement",
    },
    "ear": {
        "description": "Hold that can be held from multiple angles. Can be considered a two sided crimp",
    }
} 