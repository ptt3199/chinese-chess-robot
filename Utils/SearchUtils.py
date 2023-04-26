class SearchUtils:
    @staticmethod
    def binary_search(vlss, vl):
        low = 0
        high = len(vlss) - 1
        while low <= high:
            mid = (low + high) // 2
            if vlss[mid][0] < vl:
                low = mid + 1
            elif vlss[mid][0] > vl:
                high = mid - 1
            else:
                return mid
        return -1
