import copy
import time

from builtins import print

from Log.Logger import Logger
from AI.Position import Position
from Const.EngineConst import *


class Search:
    # this variable detect three-fold repetition in chess
    # But it's not optimal, you should replace it in the near future
    history_heap = []
    history_heap2 = []

    def __init__(self, fen, max_depth):
        self.maxDepth = max_depth
        self.position = Position()
        self.position.fromFen(fen)
        self.logger = Logger(Search.__name__)
        self.transposition_table = []
        self.limited_time_search = 5
        self.best_move = 0
        self.refutation_table = []
        for i in range(MAX_DEPTH):
            self.refutation_table.append([0, 0])

    def init_trasposition_table(self):
        self.transposition_table = []

        i = 0
        while i <= TRANSPOSITION_TABLE_SIZE:
            i += 1
            self.transposition_table.append(copy.deepcopy(EMPTY_TRANSPOSITION_ELEMENT))

    def search_root_negamax(self):

        max = self.position.depth - MATE_VALUE
        best_move = 0

        # generate all visible moves
        move_list = self.position.generate_moves()

        for [move, move_value] in move_list:
            if not self.position.make_move(move):
                continue

            score = -self.negamax()

            if score > max:
                best_move = move
                max = score

            self.position.undo_make_move(move)

        self.logger.info("used algorithm in searching is: minimax")
        self.logger.info("score is: " + str(max))
        return best_move

    def negamax(self):

        # evaluate position
        if self.position.depth == self.maxDepth:
            return self.position.evaluate_board()

        max = self.position.depth - MATE_VALUE

        move_list = self.position.generate_moves()

        for [move, move_value] in move_list:
            if not self.position.make_move(move):
                continue

            score = -self.negamax()

            if score > max:
                max = score

            self.position.undo_make_move(move)

        return max

    def search_root_negamax_alpha_beta(self, alpha, beta):
        """
        this function implement alpha-beta
        :param alpha:
        :param beta:
        :return:
        """
        # search database
        # move = self.position.bookMove()
        # if move != 0:
        #     print("from database " + str(move))
        #     return move

        # live search
        best_score = -MATE_VALUE
        best_move = 0

        move_list = self.position.generate_moves()
        for index in range(len(move_list)):
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.negamax_alpha_beta(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                return best_move
            # update alpha, best score
            if score > best_score:
                best_move = move
                best_score = score
                if score > alpha:
                    alpha = score

        self.logger.info("used algorithm in searching is: Negamax alpha-beta ")
        self.logger.info("score is: " + str(best_score))
        return best_move

    def negamax_alpha_beta(self, alpha, beta):
        """
        this method implement alpha beta
        :param alpha:
        :param beta:
        :return:
        """
        if self.position.depth == self.maxDepth:
            return self.position.evaluate_board()

        best_score = self.position.depth - MATE_VALUE

        move_list = self.position.generate_moves()
        for index in range(len(move_list)):
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.negamax_alpha_beta(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                return beta
            # update alpha, best score
            if score > best_score:
                best_score = score
                if score > alpha:
                    alpha = score

        return best_score

    def search_root_alpha_beta_move_ordering_TT(self, alpha, beta):
        """
        this function implement alpha-beta with move ordering, transposition table
        :param alpha:
        :param beta:
        :return:
        """
        # live search
        best_score = -MATE_VALUE
        best_move = 0
        move_list = self.position.generate_moves()
        self.init_trasposition_table()

        for index in range(len(move_list)):
            # find the best move to search first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.alpha_beta_move_ordering_TT(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                return best_move
            # update alpha, best_score
            if score > best_score:
                best_score = score
                best_move = move
                if score > alpha:
                    alpha = score

        self.logger.info("used algorithm in searching is: alpha - beta with move ordering, transposition table ")
        self.logger.info("score is: " + str(best_score))
        return best_move

    def alpha_beta_move_ordering_TT(self, alpha, beta):
        """
        this method implement alpha beta with move ordering
        :param alpha:
        :param beta:
        :return:
        """
        [zobrist_lock, flag, tt_value, hash_depth, TT_move] = self.probe_hash()

        if self.position.depth == self.maxDepth:
            value = self.position.evaluate_board()
            self.save_2_transposition_table(alpha, beta, value, 0)
            return value

        best_score = self.position.depth - MATE_VALUE
        best_move = 0

        move_list = self.position.generate_moves()
        if TT_move != 0:
            for index in range(len(move_list)):
                if TT_move == move_list[index][0]:
                    move_list[index][1] = MATE_VALUE
                    break
        for index in range(len(move_list)):
            # search capture move first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.alpha_beta_move_ordering_TT(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                self.save_2_transposition_table(alpha, beta, beta, move)
                return beta
            # update best_score, alpha
            if score > best_score:
                best_score = score
                best_move = move
                if score > alpha:
                    alpha = score

        self.save_2_transposition_table(alpha, beta, best_score, best_move)
        return best_score

    def search_root_negamax_alpha_beta_move_ordering(self, alpha, beta):
        """
        this function implement alpha-beta with move ordering
        :param alpha:
        :param beta:
        :return:
        """
        # live search
        best_score = -MATE_VALUE
        best_move = 0
        move_list = self.position.generate_moves()

        for index in range(len(move_list)):
            # find the best move to search first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.negamax_alpha_beta_move_ordering(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                return best_move
            # update alpha, best_score
            if score > best_score:
                best_score = score
                best_move = move
                if score > alpha:
                    alpha = score

        self.logger.info("used algorithm in searching is: alpha - beta with move ordering(search capture move first) ")
        self.logger.info("score is: " + str(best_score))
        return best_move

    def negamax_alpha_beta_move_ordering(self, alpha, beta):
        """
        this method implement alpha beta with move ordering
        :param alpha:
        :param beta:
        :return:
        """
        if self.position.depth == self.maxDepth:
            return self.position.evaluate_board()

        best_score = self.position.depth - MATE_VALUE

        move_list = self.position.generate_moves()
        for index in range(len(move_list)):
            # search capture move first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.negamax_alpha_beta_move_ordering(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                return beta
            # update best_score, alpha
            if score > best_score:
                best_score = score
                if score > alpha:
                    alpha = score

        return best_score

    def search_root(self):
        """
        this method like other search root method but it can detect three-fold repetition
        """
        move = self.search_root_negamax_alpha_beta_move_ordering_quiescence_search(-MATE_VALUE, MATE_VALUE)
        if move != 0:
            self.position.make_move(move)
            Search.history_heap.append(self.position.zobristLock)
            if len(Search.history_heap) > REPETITION_LOOP_TIMES:
                Search.history_heap.pop(0)
            self.position.undo_make_move(move)

        return move

    def search_root_negamax_alpha_beta_move_ordering_quiescence_search(self, alpha, beta):
        """
        this function implement alpha-beta with move ordering, quiescence search
        :param alpha:
        :param beta:
        :return:
        """
        # search database
        # move = self.position.bookMove()
        # if move != 0:
        #     print("from database " + str(move))
        #     return move

        # live search
        best_score = -MATE_VALUE
        best_move = 0
        move_list = self.position.generate_moves()

        for index in range(len(move_list)):
            # find the best move to search first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue

            if len(Search.history_heap) == REPETITION_LOOP_TIMES and Search.history_heap[0] == Search.history_heap[
                2] == self.position.zobristLock:
                # detect three-fold repetition
                Search.history_heap = []
                self.position.undo_make_move(move)
                continue
            elif move_value > 0 and self.position.depth == self.maxDepth:
                score = -self.quiescence_search(-beta, -alpha)
            else:
                score = -self.negamax_alpha_beta_move_ordering_quiescence_search(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                # this point can have bug
                return best_move

            # update best_score, alpha
            if score > best_score:
                best_move = move
                best_score = score
                if best_score > alpha:
                    alpha = score

        self.logger.info("used algorithm in searching is: alpha - beta ")
        self.logger.info("score is: " + str(best_score))
        return best_move

    def negamax_alpha_beta_move_ordering_quiescence_search(self, alpha, beta):
        """
        this method implement alpha beta with move ordering, quiescence search
        :param alpha:
        :param beta:
        :return:
        """
        if self.position.depth == self.maxDepth:
            return self.position.evaluate_board()

        best_score = self.position.depth - MATE_VALUE

        move_list = self.position.generate_moves()
        for index in range(len(move_list)):
            # find the best move to search first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            # try to make move
            if not self.position.make_move(move):
                continue

            if move_value > 0 and self.position.depth == self.maxDepth:
                score = -self.quiescence_search(-beta, -alpha)
            else:
                score = -self.negamax_alpha_beta_move_ordering_quiescence_search(-beta, -alpha)

            # undo make move
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                return beta

            # update best_score, alpha
            if score > best_score:
                best_score = score
                if best_score > alpha:
                    alpha = score

        return best_score

    def search_root_alpha_beta_move_ordering_quiescence_search_TT(self, alpha, beta):
        """
        this function implement alpha-beta with move ordering, quiescence search, transposition table
        :param alpha:
        :param beta:
        :return:
        """
        # search database
        # move = self.position.bookMove()
        # if move != 0:
        #     print("from database " + str(move))
        #     return move

        # live search
        self.init_trasposition_table()
        best_score = self.position.depth - MATE_VALUE
        best_move = 0

        move_list = self.position.generate_moves()
        for index in range(len(move_list)):
            # find the best move to search first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            if len(Search.history_heap2) == REPETITION_LOOP_TIMES and Search.history_heap2[0] == Search.history_heap2[
                2] == self.position.zobristLock:
                # detect three-fold repetition
                # Search.history_heap2 = []
                self.position.undo_make_move(move)
                continue
            if move_value > 0 and self.position.depth == self.maxDepth:
                score = -self.quiescence_search(-beta, -alpha)
            else:
                score = -self.negamax_alpha_beta_move_ordering_quiescence_search_TT(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                best_move = move
                self.best_move = move
                return beta
            # update alpha, best_score
            if score > best_score:
                best_score = score
                best_move = move
                self.best_move = best_move
                if score > alpha:
                    alpha = score

        self.logger.info("used algorithms: AlphaBeta, moveOrdering, quiescence search, transposition table ")
        self.logger.info("score is: " + str(best_score))
        return best_score

    def negamax_alpha_beta_move_ordering_quiescence_search_TT(self, alpha, beta):
        """
        this method implement alpha beta with move ordering, quiescence search, transposition table
        :param alpha:
        :param beta:
        :return:
        """
        TT_move = 0
        best_move = 0

        # search position into transposition table
        [zobrist_lock, flag, tt_value, hash_depth, TT_move] = self.probe_hash()
        if self.position.depth >= hash_depth and flag != NULL_FLAG:
            if flag == EXACT_FLAG:
                return tt_value
            elif flag == ALPHA_FLAG and tt_value > alpha:
                alpha = tt_value
            elif flag == BETA_FLAG and tt_value < beta:
                beta = tt_value
            # cut off
            if alpha >= beta:
                return tt_value

        if self.position.depth == self.maxDepth:
            value = self.position.evaluate_board()
            self.save_2_transposition_table(alpha, beta, value, 0)
            return value

        best_score = self.position.depth - MATE_VALUE

        move_list = self.position.generate_moves()
        if TT_move != 0:
            for index in range(len(move_list)):
                if TT_move == move_list[index][0]:
                    move_list[index][1] = MATE_VALUE
                    break
        for index in range(len(move_list)):
            # find the best move to search first
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            if move_value > 0 and self.position.depth == self.maxDepth:
                score = -self.quiescence_search(-beta, -alpha)
            else:
                score = -self.negamax_alpha_beta_move_ordering_quiescence_search_TT(-beta, -alpha)
            self.position.undo_make_move(move)

            if score > best_score:
                best_move = move
                best_score = score
            if best_score > alpha:
                alpha = best_score
            if best_score >= beta:
                break

        self.save_2_transposition_table(alpha, beta, best_score, best_move)
        return best_score

    def search_root_alpha_beta_tt(self, alpha, beta):
        """
        this function implement alpha-beta with move ordering, quiescence search, transposition table
        :param alpha:
        :param beta:
        :return:
        """
        # search database
        # move = self.position.bookMove()
        # if move != 0:
        #     print("from database " + str(move))
        #     return move

        # live search
        self.init_trasposition_table()
        best_score = self.position.depth - MATE_VALUE
        best_move = 0

        move_list = self.position.generate_moves()
        for element in move_list:
            [move, move_value] = element

            if not self.position.make_move(move):
                continue
            score = -self.alpha_beta_tt(-beta, -alpha)
            self.position.undo_make_move(move)

            if score > best_score:
                best_score = score
                best_move = move
            if best_score > alpha:
                alpha = best_score
            if best_score >= beta:
                break

        self.logger.info("used algorithms: AlphaBeta, transposition table ")
        self.logger.info("score is: " + str(best_score))
        return best_move

    def alpha_beta_tt(self, alpha, beta):
        """
        this method implement alpha beta with transposition table
        :param alpha:
        :param beta:
        :return:
        """
        TT_move = 0
        best_move = 0
        # search position into transposition table
        [zobrist_lock, flag, tt_value, hash_depth, TT_move] = self.probe_hash()
        if self.position.depth >= hash_depth and flag != NULL_FLAG:
            if flag == EXACT_FLAG:
                print("EXACT_FLAG")
                return tt_value
            elif flag == ALPHA_FLAG and tt_value > alpha:
                print("ALPHA_FLAG")
                alpha = tt_value
            elif flag == BETA_FLAG and tt_value < beta:
                print("BETA_FLAG")
                beta = tt_value
            # cut off
            if alpha >= beta:
                return tt_value

        # if get maximum depth
        if self.position.depth == self.maxDepth:
            value = self.position.evaluate_board()
            self.save_2_transposition_table(alpha, beta, value, 0)
            return value

        best_score = self.position.depth - MATE_VALUE

        move_list = self.position.generate_moves()
        if TT_move != 0:
            Search.swap_element(move_list, TT_move)
        for element in move_list:
            [move, move_value] = element

            if not self.position.make_move(move):
                continue
            score = -self.alpha_beta_tt(-beta, -alpha)
            self.position.undo_make_move(move)

            if score > best_score:
                best_move = move
                best_score = score
            if best_score > alpha:
                alpha = best_score
            if best_score >= beta:
                break

        self.save_2_transposition_table(alpha, beta, best_score, best_move)
        return best_score

    @staticmethod
    def swap_element(move_list, move):
        flag = True
        for index in range(len(move_list)):
            if move_list[index][0] == move:
                flag = False
                move_list[0], move_list[index] = move_list[index], move_list[0]

        if flag:
            print("wrong hashing")

    @staticmethod
    def selection_sort(index, list):
        # do nothing
        if index == len(list) - 1:
            return

        # find the largest element in unsorted part
        min_index = index + 1
        for i in range(index + 1, len(list)):
            if list[i][1] > list[min_index][1]:
                min_index = i

        # swap 2 element
        list[index], list[min_index] = list[min_index], list[index]

    def quiescence_search(self, alpha, beta):
        """
        this function implement quiescence search algorithm with null pruning
        :param alpha:
        :param beta:
        :return:
        """
        mate_flag = True
        check_mate_value = self.position.depth - MATE_VALUE

        # null pruning
        score = self.position.evaluate_board()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

        if self.position.depth == MAX_DEPTH:
            return score

        move_list = self.position.generate_capture_moves()
        for index in range(len(move_list)):
            self.selection_sort(index, move_list)
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.quiescence_search(-beta, -alpha)
            self.position.undo_make_move(move)

            # set flag to false
            mate_flag = False

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        if mate_flag and len(move_list) > 0:
            return check_mate_value
        else:
            return alpha

    def interative_depth_first_search(self):
        # search database
        move = self.position.bookMove()
        if move != 0:
            print("from database " + str(move))
            return move
        start_time = time.time()
        for depth in range(1, MAX_DEPTH):
            # print("history_heap" + str(Search.history_heap))
            # print("history_heap 2" + str(Search.history_heap2))
            Search.history_heap2 = Search.history_heap
            # search root by depth
            self.maxDepth = depth
            score = self.search_root_alpha_beta_move_ordering_quiescence_search_TT(-MATE_VALUE, MATE_VALUE)

            interval_time = time.time() - start_time
            print("interval time is: " + str(interval_time))
            if interval_time > self.limited_time_search:
                break
            if score < -WIN_VALUE or score > WIN_VALUE:
                break

        # return best move
        return self.best_move

    def search_root_alpha_beta_IDFS(self, alpha, beta):
        """
        this function implement alpha-beta
        :param alpha:
        :param beta:
        :return:
        """
        # search database
        # move = self.position.bookMove()
        # if move != 0:
        #     print("from database " + str(move))
        #     return move

        # live search
        best_score = -MATE_VALUE
        best_move = 0

        move_list = self.position.generate_moves()
        for index in range(len(move_list)):
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.negamax_alpha_beta_IDFS(-beta, -alpha)
            self.position.undo_make_move(move)

            # cut off
            if score >= beta:
                return best_move
            # update alpha, best score
            if score > best_score:
                best_move = move
                best_score = score
                if score > alpha:
                    alpha = score

        self.logger.info("used algorithm in searching is: Negamax alpha-beta ")
        self.logger.info("score is: " + str(best_score))
        return best_move

    def negamax_alpha_beta_IDFS(self, alpha, beta):
        """
        this method implement alpha beta
        :param alpha:
        :param beta:
        :return:
        """
        if self.position.depth == self.maxDepth:
            return self.position.evaluate_board()

        best_score = self.position.depth - MATE_VALUE

        move_list = self.position.generate_moves()
        for index in range(len(move_list)):
            [move, move_value] = move_list[index]

            if not self.position.make_move(move):
                continue
            score = -self.negamax_alpha_beta_IDFS(-beta, -alpha)
            self.position.undo_make_move(move)

            if score > self.refutation_table[self.position.depth][1]:
                zdfsdf
            # cut off
            if score >= beta:
                return beta
            # update alpha, best score
            if score > best_score:
                best_score = score
                if score > alpha:
                    alpha = score

        return best_score

    def get_hash_item(self):
        return self.transposition_table[self.position.zobristLock & TRANSPOSITION_TABLE_SIZE]

    def save_2_transposition_table(self, alpha, beta, score, move):
        """
        this method save data to transposition table
        :param alpha:
        :param beta:
        :param score:
        :param move:
        :return:
        """
        flag = EXACT_FLAG
        if score <= alpha:
            flag = ALPHA_FLAG
        elif score >= beta:
            flag = BETA_FLAG

        hash_entity = self.get_hash_item()
        if hash_entity[1] == NULL_FLAG or hash_entity[3] > self.position.depth:
            hash_entity[0] = self.position.zobristLock
            hash_entity[1] = flag
            hash_entity[2] = score
            hash_entity[3] = self.position.depth
            hash_entity[4] = move

    def probe_hash(self):
        """
        this method search state in transposition table by brorist key
        :return:
        """
        entry = self.get_hash_item()
        if entry[0] == self.position.zobristLock:
            return entry
        else:
            return EMPTY_TRANSPOSITION_ELEMENT
