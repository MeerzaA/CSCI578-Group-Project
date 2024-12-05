# Placeholder class to simulate a data stream
class DataPipe:

    # The end of the pipe to which a component writes its output data
    class OutputDataPipe:

        def write( self, item ):
            print("\n\n\nWROTE ITEM TO PIPE\n\n\n")
            self.queue.append( item ) 

        def __init__( self, queue ):
            self.queue = queue
            
    # The end of the pipe from which a compenent gets its input data
    class InputDataPipe:

        def read( self ):
           
            if len( self.queue ) > 0:
                item = self.queue[0]
                self.queue.pop(0)
                return item
            
            return None

        def __init__( self, queue ):
            self.queue = queue


    def __init__( self, name ):
        print( f"{name} initializing" )
        self.name = name
        self.queue = []
        self.output_pipe = self.OutputDataPipe( self.queue )
        self.input_pipe = self.InputDataPipe( self.queue )
        print( f"{name} initialized" )