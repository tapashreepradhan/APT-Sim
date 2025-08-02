import numpy as np

def compute_pairwise_jaccard(caseX, caseY, decimals=12):
    """
    Compute Jaccard similarity between two cases per step using vectorized numpy operations.
    Returns: dict of jaccard[step]
    """
    jaccard = {}
    for step, dfX in caseX.items():
        if step not in caseY:
            continue
        coordsX = np.round(dfX[['x', 'y', 'z']].to_numpy(), decimals)
        coordsY = np.round(caseY[step][['x', 'y', 'z']].to_numpy(), decimals)

        # Flatten the arrays and find intersection and union
        coordsX = coordsX.view([('', coordsX.dtype)] * coordsX.shape[1])
        coordsY = coordsY.view([('', coordsY.dtype)] * coordsY.shape[1])

        inter = np.intersect1d(coordsX, coordsY)
        union = np.union1d(coordsX, coordsY)
        jaccard[step] = len(inter) / len(union) if len(union) else 0.0
    return jaccard

def compute_3way_jaccard(caseA, caseB, caseC, decimals=12):
    """
    Compute 3-way Jaccard similarity across A, B, and C per step using vectorized numpy operations.
    Returns: dict of jaccard_3way[step]
    """
    jaccard_3way = {}
    for step in caseA:
        if step not in caseB or step not in caseC:
            continue
        coordsA = np.round(caseA[step][['x', 'y', 'z']].to_numpy(), decimals)
        coordsB = np.round(caseB[step][['x', 'y', 'z']].to_numpy(), decimals)
        coordsC = np.round(caseC[step][['x', 'y', 'z']].to_numpy(), decimals)

        # Flatten the arrays and find intersection and union
        coordsA = coordsA.view([('', coordsA.dtype)] * coordsA.shape[1])
        coordsB = coordsB.view([('', coordsB.dtype)] * coordsB.shape[1])
        coordsC = coordsC.view([('', coordsC.dtype)] * coordsC.shape[1])

        # Perform 3-way intersection and union
        inter = np.intersect1d(coordsA, coordsB)
        inter = np.intersect1d(inter, coordsC)
        union = np.union1d(coordsA, coordsB)
        union = np.union1d(union, coordsC)

        jaccard_3way[step] = len(inter) / len(union) if len(union) else 0.0
    return jaccard_3way

def compute_sliding_window_jaccard(caseX, caseY, window_sizes=[10, 100, 500], decimals=12):
    """
    Compute Jaccard similarity using sliding windows of different sizes.
    Returns: dict of {window_size: {start_step: jaccard_value}}
    """
    results = {}
    
    # Get all common steps
    common_steps = sorted(set(caseX.keys()) & set(caseY.keys()))
    
    for window_size in window_sizes:
        results[window_size] = {}
        
        # Slide window across the data
        for start_idx in range(0, len(common_steps), window_size):
            end_idx = min(start_idx + window_size, len(common_steps))
            window_steps = common_steps[start_idx:end_idx]
            
            if len(window_steps) == 0:
                continue
                
            # Collect all coordinates in this window
            coordsX_window = []
            coordsY_window = []
            
            for step in window_steps:
                coordsX = np.round(caseX[step][['x', 'y', 'z']].to_numpy(), decimals)
                coordsY = np.round(caseY[step][['x', 'y', 'z']].to_numpy(), decimals)
                coordsX_window.extend(coordsX)
                coordsY_window.extend(coordsY)
            
            # Convert to numpy arrays and flatten
            coordsX_window = np.array(coordsX_window)
            coordsY_window = np.array(coordsY_window)
            
            if len(coordsX_window) == 0 or len(coordsY_window) == 0:
                continue
                
            coordsX_window = coordsX_window.view([('', coordsX_window.dtype)] * coordsX_window.shape[1])
            coordsY_window = coordsY_window.view([('', coordsY_window.dtype)] * coordsY_window.shape[1])
            
            # Calculate Jaccard similarity for this window
            inter = np.intersect1d(coordsX_window, coordsY_window)
            union = np.union1d(coordsX_window, coordsY_window)
            jaccard_value = len(inter) / len(union) if len(union) else 0.0
            
            # Use the start step as the key
            results[window_size][window_steps[0]] = jaccard_value
    
    return results

def compute_sliding_window_3way_jaccard(caseA, caseB, caseC, window_sizes=[10, 100, 500], decimals=12):
    """
    Compute 3-way Jaccard similarity using sliding windows of different sizes.
    Returns: dict of {window_size: {start_step: jaccard_value}}
    """
    results = {}
    
    # Get all common steps
    common_steps = sorted(set(caseA.keys()) & set(caseB.keys()) & set(caseC.keys()))
    
    for window_size in window_sizes:
        results[window_size] = {}
        
        # Slide window across the data
        for start_idx in range(0, len(common_steps), window_size):
            end_idx = min(start_idx + window_size, len(common_steps))
            window_steps = common_steps[start_idx:end_idx]
            
            if len(window_steps) == 0:
                continue
                
            # Collect all coordinates in this window
            coordsA_window = []
            coordsB_window = []
            coordsC_window = []
            
            for step in window_steps:
                coordsA = np.round(caseA[step][['x', 'y', 'z']].to_numpy(), decimals)
                coordsB = np.round(caseB[step][['x', 'y', 'z']].to_numpy(), decimals)
                coordsC = np.round(caseC[step][['x', 'y', 'z']].to_numpy(), decimals)
                coordsA_window.extend(coordsA)
                coordsB_window.extend(coordsB)
                coordsC_window.extend(coordsC)
            
            # Convert to numpy arrays and flatten
            coordsA_window = np.array(coordsA_window)
            coordsB_window = np.array(coordsB_window)
            coordsC_window = np.array(coordsC_window)
            
            if len(coordsA_window) == 0 or len(coordsB_window) == 0 or len(coordsC_window) == 0:
                continue
                
            coordsA_window = coordsA_window.view([('', coordsA_window.dtype)] * coordsA_window.shape[1])
            coordsB_window = coordsB_window.view([('', coordsB_window.dtype)] * coordsB_window.shape[1])
            coordsC_window = coordsC_window.view([('', coordsC_window.dtype)] * coordsC_window.shape[1])
            
            # Calculate 3-way Jaccard similarity for this window
            inter = np.intersect1d(coordsA_window, coordsB_window)
            inter = np.intersect1d(inter, coordsC_window)
            union = np.union1d(coordsA_window, coordsB_window)
            union = np.union1d(union, coordsC_window)
            jaccard_value = len(inter) / len(union) if len(union) else 0.0
            
            # Use the start step as the key
            results[window_size][window_steps[0]] = jaccard_value
    
    return results
