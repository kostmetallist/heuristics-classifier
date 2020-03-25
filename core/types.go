package core 

import (
	heuError "github.com/kostmetallist/heuclassifier/error"
	"strconv"
)


type Event struct {
	id int
	activity string
	extra map[string]string
}

type EventSequence []Event
type RawTableData [][]string


func (rtd RawTableData) ToEventSequence() EventSequence {
	var result EventSequence
	for _, row := range rtd {
		var event Event
		event.extra = make(map[string]string)
		for j, elem := range row {
			switch j {
			case 0:
				var err error
				event.id, err = strconv.Atoi(elem)
				heuError.CheckError(err)
			case 1:
				event.activity = elem
			default:
				event.extra[strconv.Itoa(j)] = elem
			}
		}
		result = append(result, event)
	}
	return result
}
