from collections import defaultdict
import unittest
from tests import test_cases


def give_outline_of_boxes(boxes):
    # sorting the list based on x1
    boxes = sorted(boxes, key=lambda box: box[0])

    index_height_mapper = defaultdict()
    outline = []
    # filling all the boxes height w.r.t X - axis index
    for box in boxes:
        x1, x2, h = box
        updated_heights = {
            i: h for i in range(x1, x2+1) if (
                h > (index_height_mapper.get(i) or 0)
            )
        }
        index_height_mapper.update(updated_heights)

    # finding out outline from index_height_mapper
    last_x, last_h = None, None
    for x, h in index_height_mapper.items():
        if last_x and last_h:
            # checking if height changed
            if last_h != h:
                if (x - last_x) == 1:
                    point = None
                    if h > last_h:
                        # raise
                        point = (x, h)
                    elif h < last_h:
                        # drop
                        point = (last_x, h)
                    outline.append(point)
                else:
                    outline.append((last_x, 0))
            # gap from previous box
            if (x - last_x) > 1:
                outline.append((x, h))
        last_x, last_h = x, h
    # adding first and last point
    outline.insert(0,
                   (boxes[0][0], index_height_mapper[boxes[0][0]])
                   )
    outline.append(
        (index_height_mapper.popitem()[0], 0)
    )
    return outline


class TestOutlineAlgorithm(unittest.TestCase):
    # Returns True if output matches expected outline
    def test_outline_validity(self):
        for case in test_cases:
            output = give_outline_of_boxes(case['input'])
            self.assertEqual(output, case['output'])


if __name__ == '__main__':
    unittest.main()
