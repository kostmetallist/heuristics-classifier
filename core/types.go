package core 

type Event struct {
	id int
	activity string
	extra map[string]string
}

type EventSequence []Event
