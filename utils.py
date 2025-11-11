import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import minimum_spanning_tree

KILTERBOARD_AREA_INCHES = 27648

def extract_xy_coordinates(holds):
    """
    Extract x,y coordinates from a list of holds.
    
    Args:
        holds: List of hold dictionaries with 'x' and 'y' keys
        
    Returns:
        List of (x, y) tuples
    """
    return [(hold['x'], hold['y']) for hold in holds]

def compute_hull_area(holds):
    """
    Compute the convex hull area and perimeter for a list of holds.
    
    Args:
        holds: List of hold dictionaries with 'x' and 'y' keys
        
    Returns:
        Dictionary with 'area' and 'perimeter' values
    """
    # Extract coordinates
    coords = extract_xy_coordinates(holds)
    
    # Convert to numpy array
    pts = np.array(coords)  # shape [N,2]
    
    # Need at least 3 points for a convex hull
    if len(pts) < 3:
        return 0.0
    
    # Compute convex hull
    hull = ConvexHull(pts)  # 2D: hull.volume == area
    hull_indices = hull.vertices  # CCW order of hull vertices
    hull_points = pts[hull_indices]  # coordinates on the hull (closed if you like)
    
    # Calculate area and perimeter
    area = hull.volume  # polygon area
    area_coverage = area / KILTERBOARD_AREA_INCHES
    perim = np.linalg.norm(np.diff(np.r_[hull_points, hull_points[:1]], axis=0), axis=1).sum()
    
    return area_coverage

def mst_longest_edges(points, top_k=None):
    """
    points: iterable of (x, y)
    top_k: return only the top_k longest MST edges (None = all)

    returns: list of (i, j, length) sorted by length desc
    """
    X = np.asarray(points, dtype=float)
    # Pairwise Euclidean distances (dense)
    D = squareform(pdist(X, metric='euclidean'))
    # Minimum spanning tree on the dense matrix (returns sparse matrix)
    mst = minimum_spanning_tree(D).tocoo()

    edges = [(int(i), int(j), float(w)) for i, j, w in zip(mst.row, mst.col, mst.data)]
    edges.sort(key=lambda e: e[2], reverse=True)
    return edges if top_k is None else edges[:top_k]

def mst_average_edge(points):
    """
    Calculate the average length of edges in the minimum spanning tree.
    
    Args:
        points: iterable of (x, y) coordinates
        
    Returns:
        float: average length of edges in the MST
    """
    if len(points) < 2:
        return 0.0
    
    X = np.asarray(points, dtype=float)
    # Pairwise Euclidean distances (dense)
    D = squareform(pdist(X, metric='euclidean'))
    # Minimum spanning tree on the dense matrix (returns sparse matrix)
    mst = minimum_spanning_tree(D).tocoo()
    
    # Calculate average length of edges
    if len(mst.data) == 0:
        return 0.0
    return float(np.mean(mst.data))

def test_compute_hull_area():
    """Test the compute_hull_area function with various scenarios."""
    print("Testing compute_hull_area...")
    
    # Test 1: Square with 4 points
    square_holds = [
        {"x": 0, "y": 0},
        {"x": 10, "y": 0},
        {"x": 10, "y": 10},
        {"x": 0, "y": 10}
    ]
    result1 = compute_hull_area(square_holds)
    assert result1 > 0, f"Expected positive area coverage, got {result1}"
    
    # Test 2: Triangle with 3 points
    triangle_holds = [
        {"x": 0, "y": 0},
        {"x": 5, "y": 0},
        {"x": 2.5, "y": 5}
    ]
    result2 = compute_hull_area(triangle_holds)
    assert result2 > 0, "Triangle should have positive area coverage"
    print(f"Single point: area coverage={result2:.4f} ({result2*100:.2f}%)")

    # Test 3: Less than 3 points (edge case)
    few_holds = [
        {"x": 0, "y": 0},
        {"x": 5, "y": 0}
    ]
    result3 = compute_hull_area(few_holds)
    assert result3 == 0.0, "Two points should have zero area coverage"
    
    # Test 4: Single point
    single_hold = [{"x": 0, "y": 0}]
    result4 = compute_hull_area(single_hold)
    print(f"Single point: area coverage={result4:.4f} ({result4*100:.2f}%)")
    assert result4 == 0.0, "Single point should have zero area coverage"
    
    # Test 5: Empty list
    empty_holds = []
    result5 = compute_hull_area(empty_holds)
    print(f"Empty list: area coverage={result5:.4f} ({result5*100:.2f}%)")
    assert result5 == 0.0, "Empty list should have zero area coverage"
    
    print("All tests passed! ✅")

def test_mst_longest_edges():
    """Test the mst_longest_edges function with various scenarios."""
    print("Testing mst_longest_edges...")
    
    # Test 1: Square with 4 points
    square_points = [(0, 0), (10, 0), (10, 10), (0, 10)]
    result1 = mst_longest_edges(square_points)
    print(f"Square (4 points): {len(result1)} edges found")
    print(f"Longest edge: {result1[0] if result1 else 'None'}")
    
    # Test 2: Triangle with 3 points
    triangle_points = [(0, 0), (5, 0), (2.5, 5)]
    result2 = mst_longest_edges(triangle_points)
    print(f"Triangle (3 points): {len(result2)} edges found")
    print(f"Longest edge: {result2[0] if result2 else 'None'}")
    
    # Test 3: Line with 3 points
    line_points = [(0, 0), (5, 0), (10, 0)]
    result3 = mst_longest_edges(line_points)
    print(f"Line (3 points): {len(result3)} edges found")
    print(f"Longest edge: {result3[0] if result3 else 'None'}")
    
    # Test 4: With top_k parameter
    many_points = [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1)]
    result4 = mst_longest_edges(many_points, top_k=2)
    print(f"Many points (top_k=2): {len(result4)} edges found")
    print(f"Top 2 edges: {result4}")
    
    # Test 5: Single point (edge case)
    single_point = [(0, 0)]
    result5 = mst_longest_edges(single_point)
    print(f"Single point: {len(result5)} edges found")
    
    # Test 6: Two points (edge case)
    two_points = [(0, 0), (5, 0)]
    result6 = mst_longest_edges(two_points)
    print(f"Two points: {len(result6)} edges found")
    
    print("All MST tests completed! ✅")

def main():
    """Run all tests."""
    test_compute_hull_area()
    print("\n" + "="*50 + "\n")
    test_mst_longest_edges()

if __name__ == "__main__":
    main()


