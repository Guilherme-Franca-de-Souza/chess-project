 """    
    fen = '8/3K3B/4p2P/2p1k1p1/8/p7/8/8 w - - 0 1'
    board = chess.Board(fen)
    try:
        while True:
            classical_best_lines = get_best_lines(classical, board, depth=3)
            for i, line_info in enumerate(classical_best_lines):
                print('\n\n')
                score = line_info['score'].relative.score(mate_score=10000)
                #line = line_info['pv']
                #line_str = get_line_str(line) 
                print(f"Classical Score = {score}")
            nnue_best_lines = get_best_lines(nnue, board, depth=3)
            for i, line_info in enumerate(nnue_best_lines):
                print('\n\n')
                score = line_info['score'].relative.score(mate_score=10000)
                #line = line_info['pv']
                #line_str = get_line_str(line) 
                print(f"NNUE Score = {score}")
            another_best_lines = get_best_lines(another, board, depth=3)
            for i, line_info in enumerate(another_best_lines):
                print('\n\n')
                score = line_info['score'].relative.score(mate_score=10000)
                #line = line_info['pv']
                #line_str = get_line_str(line) 
                print(f"NNUE Score = {score}")
            
        
            time.sleep(1)
    except Exception as e:
        print(f"Engine error: {e} ")
    """