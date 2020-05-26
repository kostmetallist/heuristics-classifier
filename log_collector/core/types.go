package core 

import "strconv"

type RawTableData [][]string
type Event map[string]interface{}
type EventSequence []Event

func EmptyEvent() (Event, error) {
	return make(Event), nil
}

func (rtd RawTableData) ToEventSequence() EventSequence {
	var result EventSequence
	var columnNames []string
	for i, row := range rtd {
		if i == 0 {
			columnNames = make([]string, len(row))
			for j, elem := range row {
				columnNames[j] = elem
			}

		} else {
			event, _ := EmptyEvent()
			for j, elem := range row {
				correspondingColumn := columnNames[j]
				if intValue, err := strconv.ParseInt(elem, 10, 0); err == nil {
					event[correspondingColumn] = intValue
					continue
				}
				if floatValue, err := strconv.ParseFloat(elem, 64); err == nil {
					event[correspondingColumn] = floatValue
					continue
				}
				if boolValue, err := strconv.ParseBool(elem); err == nil {
					event[correspondingColumn] = boolValue
					continue
				}
				if elem == "null" {
					event[correspondingColumn] = nil
					continue
				}
				// processing string type here
				if len(elem) == 0 {
					event[correspondingColumn] = nil
				} else {
					event[correspondingColumn] = elem
				}
			}
			result = append(result, event)
		}
	}
	return result
}
