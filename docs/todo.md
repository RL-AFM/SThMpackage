#todo

- ~~Save probe data al at once~~
- Implement the four terminal resistance estimation from fourTermResistance.py
- Add dots to current sweep plots
- Fix resistance plots to be based upon $V_{out}(ax^3)$
- ~~Ensure correct scaling of C319 bridge data (saved by ```input_bridge_test()```)~~


- ~~The max current calculation is not correct for standard KNT probes. In fact, the class has only been set up to handle novel probes, and not the regular ones we will be using as a control.~~
  - ~~I'd like to move from having seperate type and size variables into one type. Then we can have all options C1-4, N1-4 and K. If it's K, set max current to 2mA and have done with. Otherwise, deal with appropiately for the novel types~~
  - ~~Issue is that this breaks compatibility with the previously saved JSON probe types. However, given there are only a small number of them, it might be worth it to just manually change entries. This is why we went with JSON, right? Because its more human readable and editable than just pickling our outout~~
