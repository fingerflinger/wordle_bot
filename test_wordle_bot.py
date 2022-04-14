import wordle_bot

def test_find_idx_in_active_digits():
    loc = wordle_bot.find_idx_in_active_digits('spear', [False, True, True, True, True], 'e')
    assert(loc == 2)
    loc = wordle_bot.find_idx_in_active_digits('spear', [False, True, False, True, True], 'e')
    assert(loc == -1)
    loc = wordle_bot.find_idx_in_active_digits('aares', [False, True, True, True, True], 'a')
    assert(loc == 1)
    loc = wordle_bot.find_idx_in_active_digits('araes', [False, True, True, True, True], 'a')
    assert(loc == 2)
    loc = wordle_bot.find_idx_in_active_digits('araes', [False, False, True, True, True], 'a')
    assert(loc == 2)

def test_pattern_from_guess():
    pattern = wordle_bot.pattern_from_guess('lares', 'black')
    assert(pattern == [1, 1, 2, 2, 2])
    pattern = wordle_bot.pattern_from_guess('lares', 'royal')
    assert(pattern == [1, 1, 1, 2, 2])

def test_do_solve():
    assert(wordle_bot.do_solve("vapes") == False)
    assert(wordle_bot.do_solve("royal") == "royal")
    assert(wordle_bot.do_solve("black") == "black")
    assert(wordle_bot.do_solve("stair") == "stair")
    assert(wordle_bot.do_solve("stand") == "stand")
