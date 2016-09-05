
function init_notebook() {
    IPython.notebook.kernel.restart();
    $(IPython.events).one(  'kernel_ready.Kernel',
                            function(){ IPython.notebook.execute_all_cells(); }
    );
}
