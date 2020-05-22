package core 

import (
	heuError "github.com/kostmetallist/heuclassifier/log_collector/error"
	"strconv"
)

type Event struct {
	Id int
	Activity string
	Extra map[string]string
}

type EventSequence []Event
type RawTableData [][]string

func (rtd RawTableData) ToEventSequence() EventSequence {
	var result EventSequence
	for _, row := range rtd {
		var event Event
		event.Extra = make(map[string]string)
		for j, elem := range row {
			switch j {
			case 0:
				var err error
				event.Id, err = strconv.Atoi(elem)
				heuError.CheckError(err)
			case 1:
				event.Activity = elem
			default:
				event.Extra[strconv.Itoa(j)] = elem
			}
		}
		result = append(result, event)
	}
	return result
}
