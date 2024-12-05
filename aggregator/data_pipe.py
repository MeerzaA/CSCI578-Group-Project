# Thread-safe queue
from queue import Queue

# Placeholder class to simulate a data stream
class DataPipe:

    # The end of the pipe to which a component writes its output data
    class OutputDataPipe:

        def write( self, item ):
            self.queue.put( item ) 
            print("\nWROTE ITEM TO PIPE\n")

        def __init__( self, queue ):
            self.queue = queue
            
    # The end of the pipe from which a compenent gets its input data
    class InputDataPipe:

        def read( self ):
           
            if self.queue.empty():
                return None

            print("\nREAD ITEM FROM PIPE\n")
            return self.queue.get()
            

        def __init__( self, queue ):
            self.queue = queue


    def __init__( self, name ):
        print( f"{name} initializing" )
        self.name = name
        self.queue = Queue()
        self.output_pipe = self.OutputDataPipe( self.queue )
        self.input_pipe = self.InputDataPipe( self.queue )
        print( f"{name} initialized" )