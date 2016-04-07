package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	. "os"
	"strconv"
	"strings"

	"github.com/layeh/gumble/gumble"
	"github.com/layeh/gumble/gumbleutil"
)

func main() {
	// flags and pos args
	var output, username, server, port, channel, comment string
	flag.StringVar(&output, "output", "output.txt", "Output file for collection")
	flag.StringVar(&server, "server", "127.0.0.1", "Server address of Mumble server")
	flag.StringVar(&port, "port", "64738", "Port for Mumble server")
	flag.StringVar(&username, "username", "CollectionBot", "Username of bot")
	flag.StringVar(&channel, "channel", "root", "Default channel for bot")
	flag.StringVar(&comment, "comment", "I collect text for use in training Markov Chains", "Default comment for bot")
	flag.Parse()

	// check if output exists, if it doesn't create it first
	var f *File
	var err error
	if f, err = os.OpenFile(output, O_RDWR|O_APPEND|O_CREATE, 0644); err != nil {
		panic(err)
	}
	w := bufio.NewWriter(f)

	// keep alive chan
	keep := make(chan bool)

	// mumble related
	config := gumble.Config{
		Username: username,
		Address:  server + ":" + port,
	}
	client := gumble.NewClient(&config)
	config.TLSConfig.InsecureSkipVerify = true
	defaultChannel := strings.Split(channel, "/")

	// just for convenience
	words := 0

	// listeners
	client.Attach(gumbleutil.Listener{
		Connect: func(e *gumble.ConnectEvent) {
			if client.Channels.Find(defaultChannel...) != nil {
				client.Self.Move(client.Channels.Find(defaultChannel...))
			} else {
				fmt.Println("Could not find channel", defaultChannel)
			}
			if client.Self.IsRegistered() == false {
				client.Self.Register()
			}
			client.Self.SetComment(comment + "<br><br>Stored " + strconv.Itoa(words) + " lines this session")
		},
		TextMessage: func(e *gumble.TextMessageEvent) {
			if u := e.Sender; u != nil {
				fmt.Println("Caught:", e.Message)
				w.WriteString(e.Message + "\n")
				w.Flush()

				words++
				client.Self.SetComment(comment + "<br><br>Stored " + strconv.Itoa(words) + " lines this session")
			}
		},
		Disconnect: func(e *gumble.DisconnectEvent) {
			keep <- true
		},
	})

	// connect
	if err := client.Connect(); err != nil {
		fmt.Println("Could not connect to server", config.Address)
		os.Exit(1)
	}

	// keep it connected, yo
	<-keep

	// on finish
	defer w.Flush()
	defer f.Close()

	// TODO: handle ^C via os.Signal & signal.Notify (with os.Interrupt)?
}
