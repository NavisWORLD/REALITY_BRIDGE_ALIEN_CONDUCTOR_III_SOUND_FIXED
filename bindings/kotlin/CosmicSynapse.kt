package realitybridge.synaptic

/**
 * First-party Kotlin/JVM facade for Synaptic Core v1.
 * Numerical behavior is delegated to the canonical Java implementation in the
 * same package so Java and Kotlin cannot drift apart.
 */
class CosmicSynapse @JvmOverloads constructor(
    config: Synapse.Config = Synapse.Config()
) {
    private val core = Synapse(config)

    val state: Synapse.State
        get() = core.state()

    fun pulse(input: Double, modulation: Double = 0.0, dtSeconds: Double = 0.01): Double =
        core.pulse(input, modulation, dtSeconds)

    fun step(input: Double, modulation: Double = 0.0, dtSeconds: Double = 0.01): Double =
        core.step(input, modulation, dtSeconds)

    fun reinforce(reward: Double) = core.reinforce(reward)

    fun couple(sourceOutput: Double, strength: Double) = core.couple(sourceOutput, strength)

    fun reset() = core.reset()

    fun restore(state: Synapse.State) = core.restore(state)
}
