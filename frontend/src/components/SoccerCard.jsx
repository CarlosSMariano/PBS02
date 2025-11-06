export const SoccerCard = (props) => {
    console.log(props.type)
    return (
        <div className="w-full rounded-3xl hover:scale-105 transition-all duration-500 overflow-hidden text-center pb-6 bg-gradient-to-b from-gray-800 to-gray-900 flex flex-col justify-between shadow-2xl hover:shadow-yellow-500/20 border border-gray-600">
            <div className="text-center">

                <div className="px-4 py-3">
                    <h1 className={`font-bold uppercase text-lg tracking-wide ${
                        props.type == 'gol' 
                            ? "text-yellow-500 bg-yellow-500/10 px-4 py-2 rounded-full inline-block" 
                            : "text-white"
                    }`}>
                        {props.team}
                    </h1>
                </div>

                <div className="relative">
                    <img 
                        src={`/images/${props.name}.jpg`} 
                        alt={props.name} 
                        className="w-full h-64 object-cover transition-all duration-300 hover:brightness-110" 
                    />

                    <div className="absolute bottom-0 left-0 w-full h-16 bg-gradient-to-t from-gray-900 to-transparent"></div>
                </div>

                <div className="p-6">
                    <h2 className="text-2xl font-bold text-white mb-2 tracking-tight">
                        {props.name}
                    </h2>
                    
                    
                    {props.type == 'gol' ? (
                        <div className="animate-pulse mt-3">
                            <p className="text-yellow-500 uppercase font-black text-xl tracking-widest bg-yellow-500/10 px-4 py-2 rounded-full border border-yellow-500/30">
                                ⚽ GOOOOOOL!
                            </p>
                        </div>
                    ):(<p className="text-green-400 text-sm font-medium uppercase tracking-wide bg-green-400/10 px-3 py-1 rounded-full inline-block mb-3 border border-green-400/20">
                            ⚽ Com a bola
                        </p>)}
                </div>
            </div>

            {/* Badge decorativa */}
            <div className="px-6">
                <div className="w-full h-1 bg-gradient-to-r from-transparent via-gray-600 to-transparent rounded-full"></div>
            </div>
        </div>
    );
}