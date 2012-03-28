import datetime
import time
import enum

# Helpful functions used by this package.
def total_seconds (timedelta):
   # Included in timedelta starting in Python 2.7.
   return float (timedelta.microseconds + (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

def formatted_time (timedelta):
   minutes = timedelta.seconds / 60
   return "%02d:%02d:%02d" % (minutes           / 60,
                              minutes           % 60,
                              timedelta.seconds % 60)

# State enumeration used by the Timer class.
Timer_State = enum.Enum (["stopped", "running", "completed"])

class Timer:
   Zero = datetime.timedelta (0, 0, 0)

   def __init__ (self):
      self.reset ()

   def start (self):
      self.state = Timer_State.running
      self.started = datetime.datetime.now ()
      # We add a fudge second to make the time remaining look correct,
      # in place of displaying the ceiling of the fractional seconds.
      if self.duration != Timer.Zero:
         self.ending = self.started + self.duration + datetime.timedelta (seconds = 1)

   def reset (self):
      self.state    = Timer_State.stopped
      self.started  = None
      self.duration = Timer.Zero
      self.ending   = None

   def update_state (self): # Internal operation.
      if self.state == Timer_State.running and self.ending is not None and datetime.datetime.now () >= self.ending:
         self.state = Timer_State.completed

   def running (self):
      return self.state == Timer_State.running

   def set (self, duration):
      if self.state == Timer_State.running:
         raise Exception ("Can't set duration while running.")
      else:
         self.duration = duration

   def elapsed (self):
      self.update_state ()

      # Examine to see if only the time state alone can be used in the conditions.
      if self.state == Timer_State.completed:
         return formatted_time (self.duration)
      elif self.started is None:
         return formatted_time (datetime.timedelta (0) )
      else:
         return formatted_time (datetime.datetime.now () - self.started)

   def remaining (self):
      self.update_state ()

      # Examine to see if only the time state alone can be used in the conditions.
      if self.state == Timer_State.completed:
         return formatted_time (datetime.timedelta (0) )
      elif self.started is None and self.duration != Timer.Zero:
         return formatted_time (self.duration);
      elif self.ending is None:
         return formatted_time (datetime.timedelta (0) )
      else:
         return formatted_time (self.ending - datetime.datetime.now () )

   def progress (self):
      self.update_state ()

      # Examine to see if only the time state alone can be used in the conditions.
      if self.state == Timer_State.completed:
         return 1.0
      elif self.started is None or self.duration == Timer.Zero:
         return 0.0
      else:
         return total_seconds (datetime.datetime.now () - self.started) / total_seconds (self.duration)

   def seconds_remaining (self):
      self.update_state ()

      # Examine to see if only the time state alone can be used in the conditions.
      if self.started is None or self.duration == Timer.Zero or self.state != Timer_State.running:
         return 0
      else:
         return total_seconds(self.ending - datetime.datetime.now () )

   def __str__(self):
      self.update_state ()

      return "Time elapsed: " + self.timeelapsed () + "\n" + \
             "Time remaining: " + self.timeremaining() + "\n" + \
             ("Progress: %2f" % self.progress() )

class TimeInput:
   def __init__ (self):
      self.clear ()

   def clear (self):
      self.digits = '0' * 6

   def append (self, key):
      if key.isdigit ():
         self.digits = self.digits [1:] + key
      else:
         raise ValueError ("Could not append '" + key + "' to TimeInput object")

   def duration (self):
      return datetime.timedelta \
         (hours = int (self.digits [0:2]), minutes = int (self.digits [2:4]), seconds = int (self.digits [4:6]) )

   def duration_until (self):
      # self.duration represents a target time, not a time delta.
      target_seconds = int (total_seconds (self.duration () ) )
      target_time = datetime.datetime.now ().replace \
         (hour = target_seconds / 60 / 60, minute = target_seconds / 60 % 60, second = target_seconds % 60)

      if target_time <= datetime.datetime.now ():
         raise ValueError ("Time entered has already occured.")

      return target_time - datetime.datetime.now ()

   def to_string (self):
      return self.digits [0:2] + ':' + self.digits [2:4] + ':' + self.digits [4:6]

   def __str__ (self):
      return self.to_string ()

if __name__ == '__main__':
   print "Timer demo"
   timer1 = Timer ()
   timer1.set (datetime.timedelta (minutes = 10) )
   print timer1
   timer1.start ()
   for I in range (10):
      time.sleep (1)
      print timer1
