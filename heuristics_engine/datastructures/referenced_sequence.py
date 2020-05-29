from copy import deepcopy


class ReferencedSequence:

    def __init__(self, values):
        self.content = {
            'values': deepcopy(values),
            'refs': [set() for i in range(len(values))],
        }

    def _check_pattern_integration(self, pattern, from_index):
        # guarding index out of range case
        if from_index + len(pattern) > len(self.content['values']):
            return False
        for i in range(len(pattern)):
            if pattern[i] != self.content['values'][from_index+i]:
                return False
        return True

    def _count_pattern_matches(self, pattern, from_index):
        repeatsDetected = 0
        index = from_index
        while index < len(self.content['values']):
            if self._check_pattern_integration(pattern, index):
                repeatsDetected += 1
                index += len(pattern)
            else:
                break
        return repeatsDetected

    def _adjust_references(self, pattern_size, pivot_index, repeats):
        for n in range(1, repeats+1):
            for i in range(pattern_size):
                aligned_refs = set()
                for ref in self.content['refs'] \
                                       [pivot_index + pattern_size*n + i]: 

                    if ref >= pivot_index:
                        aligned_refs.add(
                            pivot_index + (ref-pivot_index)%pattern_size)
                    else:
                        aligned_refs.add(ref)

                self.content['refs'][pivot_index+i].union(aligned_refs)

    def reduce_loops(self):
        values = self.content['values']
        pivot_index = 0
        while pivot_index < len(values):
            for i in range(pivot_index+1, len(values)):
                if values[pivot_index] == values[i]:
                    pattern = values[pivot_index:i]
                    repeats = self._count_pattern_matches(pattern, i)
                    if repeats:
                        self.content['refs'][i-1].add(pivot_index)
                        self._adjust_references(
                            len(pattern), pivot_index, repeats)
                        until = i + len(pattern)*repeats

                        del values[i:until]
                        del self.content['refs'][i:until]
                        # assigning to -1 for setting `pivot_index` to zero 
                        # after breaking the inner loop
                        pivot_index = -1
                        break
                        
            pivot_index += 1

    def _retrieve_appendix_start_index(self):
        '''
        Get start index of appendix in the current content['values'].

        Appendix is considered as a postfix of a sequence, following the
        element referring to the very begginning of the sequence. For instance,
        let `seq` = [a, b, c, a, b, c, d, e]. After applying reduce_loops, 
        it becomes [a, b, c (->0), d, e]. Then, [d, e] is an appendix as it
        resides after the 'c' element, which references to the start of `seq`.
        '''
        values = self.content['values']
        for i in range(len(values)-1, -1, -1):
            if 0 in self.content['refs'][i]:
                return i+1 if i+1 != len(values) else -1
        return 0

    def is_cyclic(self):
        appendix_start = self._retrieve_appendix_start_index()
        if appendix_start == -1:
            return True
        return False
            

    def is_pseudocyclic(self):
        if self.is_cyclic():
            return True
        values = self.content['values']
        appendix_start = self._retrieve_appendix_start_index()
        appendix = values[appendix_start:]
        for i in range(len(appendix)):
            if values[appendix_start+i] != appendix[i]:
                return False
        return True


if __name__ == '__main__':
    from sys import argv
    # processing all the argv entries starting from index 1 as elements of
    # list containing string values, e.g. 
    # `python3 referenced_sequence.py a b c a b c a`
    if len(argv) > 1:
        rseq = ReferencedSequence(argv[1:])
        rseq.reduce_loops()
        print('after reducing:')
        print(rseq.content['values'])
        print(rseq.content['refs'])
        print(f'test for pseudocyclic: {rseq.is_pseudocyclic()}')
        print(f'test for cyclic: {rseq.is_cyclic()}')
    else:
        from sys import stderr
        print('given sequence is empty, aborting...', file=stderr)
